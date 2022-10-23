import { processAudioFile } from '../../utils/';
import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const UploadButton = () => {
  const onChange = (event: React.FormEvent) => {
    const files = (event.target as HTMLInputElement).files;
    if (files != null && files.length > 0) {
      processAudioFile(files[0])
        // TODO: call the backend api here with the processed file
        .then(file => console.log(file))
        .catch(err => console.error(err));
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
