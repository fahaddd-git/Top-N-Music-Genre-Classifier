import { useState } from 'react';
import {
  Container,
  Typography,
} from '@mui/material';
import { UploadButton } from '../components';

export const HomePage = () => {
  const [results, setResults] = useState({});

  return (
    <Container>
      <Container sx={{ my: 2 }}>
        <Typography>
          Instructions to go here
        </Typography>
      </Container>
      <Container sx={{ mt: 2 }}>
        <UploadButton setResults={setResults}/>
      </Container>
      <Container sx={{ mt: 2 }}>
        {
          Object.entries(results).map(([key, value]) => {
            return (
              <>
                <span>{key}: </span>
                <span>{value as number}</span>
                <br/>
              </>
            );
          })
        }
      </Container>
    </Container>
  );
};
