import { processAudioFile } from '../../utils/';
import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const UploadButton = ({ setResults }: any) => {
  const onChange = (event: React.FormEvent) => {
    const files = (event.target as HTMLInputElement).files;
    if (files != null && files.length > 0) {
      processAudioFile(files[0])
        .then(async (file) => setResults(await uploadFile(file)))
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

const uploadFile = async (file: File): Promise<object> => {
  const data = new FormData();
  data.append('file', file);
  const response = await fetch('/api/predict-genres/', {
    method: 'POST',
    body: data,
  });
  return await response.json();
};
