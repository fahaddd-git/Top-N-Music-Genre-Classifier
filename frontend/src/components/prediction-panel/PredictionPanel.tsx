import {
  Container,
  Button,
} from '@mui/material';
import { useGetPredictions } from './hooks/useGetPredictions';
import FileUploadIcon from '@mui/icons-material/FileUpload';

export const PredictionPanel = () => {
  const { loading, error, predictions, getPredictions } = useGetPredictions();

  const onChange = (event: React.FormEvent) => {
    const files = (event.target as HTMLInputElement).files;
    if (files != null && files.length > 0) {
      getPredictions(files[0]);
    }
  };

  return (
    <>
      <Container sx={{ mt: 2 }}>
        <UploadButton onChange={onChange} loading={loading} />
      </Container>
      { predictions !== null && <Container sx={{ mt: 2 }}>
        {
          Object.keys(predictions).map((key, i) => {
            return (
              <div key={i}>{key}: {(100 * predictions[key]).toFixed(3)}%</div>
            );
          })
        }
      </Container>
      }
    </>
  );
};

type UploadButtonProps = {
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  loading: boolean;
};

export const UploadButton = ({ onChange, loading }: UploadButtonProps) => {
  return (
    <Button
      variant="contained"
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
