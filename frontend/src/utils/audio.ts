const MIN_AUDIO_LENGTH = 30;  // seconds

/**
 * Validates and preprocesses an uploaded audio file
 * @return Promise that resolves to a 30-second clip of the passed audio file
 */
export async function processAudioFile (audioFile: File): Promise<File> {
  if (!audioFile.type.startsWith('audio')) {
    return await Promise.reject(new Error('Not an audio file type'));
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
        });
    };

    reader.onerror = reject;
    reader.readAsArrayBuffer(audioFile);
  });
}
