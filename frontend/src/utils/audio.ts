const MIN_AUDIO_LENGTH = 30;  // seconds
const MAX_FILE_SIZE_MB = 50;

/**
 * Validates and preprocesses an uploaded audio file
 */
export async function processAudioFile (audioFile: File): Promise<File> {
  if (!audioFile.type.startsWith('audio')) {
    return await Promise.reject(new Error('Not an audio file type'));
  }
  if (audioFile.size > (MAX_FILE_SIZE_MB * 1024 * 1024)) {
    return await Promise.reject(new Error(`Audio file must be less than ${MAX_FILE_SIZE_MB} MB`));
  }

  return await new Promise((resolve, reject) => {
    const context = new AudioContext();
    const reader = new FileReader();

    reader.onload = () => {
      const buffer = reader.result as ArrayBuffer;
      context.decodeAudioData(buffer)
        .then((audioData) => {
          if (audioData.duration < MIN_AUDIO_LENGTH) {
            reject(new Error(`Audio file must be at least ${MIN_AUDIO_LENGTH}s`));
          } else {
            resolve(audioFile);
          }
        })
        .catch(err => {
          console.error(err);
          reject(new Error('Error processing audio file. Try a different file.'));
        });
    };

    reader.onerror = reject;
    reader.readAsArrayBuffer(audioFile);
  });
}
