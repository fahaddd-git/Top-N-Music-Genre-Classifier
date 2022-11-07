export type PredictionAPIValidationErrorResponse = { detail: ValidationErrorDetail[] };
export type PredictionAPIClientErrorResponse = { detail: string };

type ValidationErrorDetail = {
  loc: string[];
  msg: string;
  type: string;
};

export function isPredictionAPIValidationErrorResponse (
  object: any
): object is PredictionAPIValidationErrorResponse {
  return Array.isArray(object?.detail) && object?.detail?.msg !== undefined;
}

export function isPredictionAPIClientErrorResponse (
  object: any
): object is PredictionAPIClientErrorResponse {
  return typeof (object?.detail) === 'string';
}
