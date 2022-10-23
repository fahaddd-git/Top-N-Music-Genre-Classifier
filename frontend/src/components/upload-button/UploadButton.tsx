import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const UploadButton = () => {
  const minimumAudioLength = 30;  // seconds

  const onChange = (event: React.FormEvent) => {
    const files = (event.target as HTMLInputElement).files;
    if (files != null && files.length > 0) {
      const theFile = files[0];
      console.log('file is ', theFile);
      decode(theFile);
    }
  };

  const decode = (f: File) => {
    const context = new AudioContext();
    const reader = new FileReader();

    reader.readAsArrayBuffer(f);
    reader.onload = () => {
      const buffer = reader.result as ArrayBuffer;
      context.decodeAudioData(buffer)
        .then(audioData => {
          if (audioData.duration < minimumAudioLength) {
            alert(`Audio file must be at least ${minimumAudioLength}s`);
          } else {
            getPrediction(audioData);
          }
        })
        .catch(err => console.error(err));
    };
  };

  const getPrediction = (f: AudioBuffer) => {
    console.log('TODO: call /api/predict-genres with', f);
  };

  return (
    <Button variant="contained" component="label">
      <FileUploadIcon sx={{ m: -0.5, mr: 1 }} />
      Upload Audio File
      <input
        hidden
        accept="audio/*"
        type="file"
        onChange={(e) => onChange(e)}
      />
    </Button>
  );
};
