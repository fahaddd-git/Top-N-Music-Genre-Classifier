import {
  isFastAPIClientErrorResponse,
  isFastAPIValidationErrorResponse,
} from './types';

/** Genre-number pairs. Numbers are decimals representing percent confidence. */
export type PredictGenresResult = { [key: string]: number };
export type PredictGenresError = Error;

export class PredictGenresClient {
  private readonly predictGenresEndpoint: string;

  constructor () {
    this.predictGenresEndpoint = '/api/predict-genres/';
  }

  /**
   * Standardize all possible server error responses
   */
  private async standardizeErrorMessage (response: Response): Promise<string> {
    try {
      const errorResponse = await response.json();
      if (isFastAPIValidationErrorResponse(errorResponse)) return errorResponse.detail[0].msg;
      if (isFastAPIClientErrorResponse(errorResponse)) return errorResponse.detail;
    } catch {
      try {
        // FastAPI returns text on 500s (https://fastapi.tiangolo.com/tutorial/handling-errors)
        return await response.text();
      } catch (error) {
        // we shouldn't get here, but if we do, better to gracefully return an expected error
        console.error(error);
      }
    }
    return 'Server error';
  }

  /** Fetch audio file predictions */
  async fetchPredictions (audioFile: File): Promise<PredictGenresResult | PredictGenresError> {
    const data = new FormData();
    data.append('file', audioFile);
    const response = await fetch(this.predictGenresEndpoint, {
      method: 'POST',
      body: data,
    });

    if (!response.ok) {
      const errorMessage = await this.standardizeErrorMessage(response);
      return await Promise.reject(new Error(errorMessage));
    }

    return await response.json();
  }
}
