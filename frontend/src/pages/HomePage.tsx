import {
  Container,
  Typography,
} from '@mui/material';
import { UploadButton } from '../components';

export const HomePage = () => {
  return (
    <Container>
      <Container sx={{ my: 2 }}>
        <Typography>
          Instructions to go here
        </Typography>
      </Container>
      <Container sx={{ mt: 2 }}>
        <UploadButton />
      </Container>
      <Container sx={{ mt: 2 }}>
        <Typography>
          Results to go here
        </Typography>
      </Container>
    </Container>
  );
};
