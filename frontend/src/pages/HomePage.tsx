import {
  Container,
  Typography,
} from '@mui/material';
import { PredictionPanel } from 'src/components';

export const HomePage = () => {
  return (
    <Container>
      <InstructionsPanel />
      <PredictionPanel />
    </Container>
  );
};

const InstructionsPanel = () => (
  <Container sx={{ mt: 2 }}>
    <Typography variant="h6">
      Instructions
    </Typography>
    <Typography>
      Upload an audio file of at least 30s in length to see the genre prediction
      results.
    </Typography>
  </Container>
);
