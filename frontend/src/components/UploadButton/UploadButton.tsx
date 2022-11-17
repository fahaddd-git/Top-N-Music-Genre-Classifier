import { Button } from '@mui/material';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export type UploadButtonProps = {
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  loading: boolean;
};

export const UploadButton = (props: UploadButtonProps) => {
  const { onChange, loading } = props;

  return (
    <Button
      variant="contained"
      // MUI documentation suggests using a hidden native <input> for uploads and rendering the
      // button element as a label; see https://mui.com/material-ui/react-button/#upload-button
      component="label"
      disabled={loading}
    >
      <FileUploadIcon sx={{ m: -0.5, mr: 1 }} />
      { loading ? 'Loading...' : 'Upload Audio File' }
      <input
        hidden
        accept="audio/*"
        type="file"
        onChange={onChange}
      />
    </Button>
  );
};
