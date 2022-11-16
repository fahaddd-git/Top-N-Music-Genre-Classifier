import { useState, useCallback } from 'react';
import {
  PredictGenresClient,
  type PredictGenresResult,
  type PredictGenresError,
} from 'src/clients';
import { processAudioFile } from 'src/utils';

/**
 * Hook to fetch genre predictions. Loading is set to true while results are being awaited,
 * and error is set to a user-friendly message if the API call fails.
 */
export const useGetPredictions = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<PredictGenresResult | null>(null);

  // wrapping in a callback makes it easier to use without relying on function wrappers
  // or similar tricks in upstream effect hooks
  const getPredictions = useCallback(async (audioFile: File) => {
    setLoading(true);
    setError(null);

    let processedAudioFile = null;
    try {
      processedAudioFile = await processAudioFile(audioFile);
    } catch (error) {
      setError((error as Error)?.message ?? 'Error processing audio file. Try a different file.');
    }

    if (processedAudioFile !== null) {
      const predictGenresClient = new PredictGenresClient();
      try {
        const predictions = await predictGenresClient.fetchPredictions(processedAudioFile);
        setPredictions(predictions as PredictGenresResult);
      } catch (error) {
        const errorMessage = (error as PredictGenresError).message;
        setError(errorMessage);
      }
    }

    setLoading(false);
  }, []);

  return { loading, error, predictions, getPredictions };
};
