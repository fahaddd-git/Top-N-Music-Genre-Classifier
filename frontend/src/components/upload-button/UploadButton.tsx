import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const UploadButton = () => (
  <Button variant="contained" component="label">
    <FileUploadIcon sx={{ m: -0.5, mr: 1 }} />
    Upload Audio File
    <input hidden accept="audio/*" type="file" />
  </Button>
);
