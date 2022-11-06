import { PredictGenresClient } from '../../clients';
import { processAudioFile } from '../../utils/';
import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const UploadButton = ({ setResults }: any) => {
  const onChange = (event: React.FormEvent) => {
    const predictGenresClient = new PredictGenresClient();
    const files = (event.target as HTMLInputElement).files;
    if (files != null && files.length > 0) {
      processAudioFile(files[0])
        .then(async (file) => setResults(await predictGenresClient.fetchPredictions(file)))
        .catch(err => alert(err));
    }
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
