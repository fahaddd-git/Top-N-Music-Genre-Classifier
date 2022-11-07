import {
  Container,
  Typography,
} from '@mui/material';
import { PredictionPanel } from 'src/components';

export const HomePage = () => {
  return (
    <Container style={ { textAlign: 'center' } }>
      <Container sx={{ my: 2 }}>
        <Typography>
          Upload an audio file of at least 30s in length to see the genre prediction
          results.
        </Typography>
      </Container>
      <PredictionPanel />
    </Container>
  );
};
