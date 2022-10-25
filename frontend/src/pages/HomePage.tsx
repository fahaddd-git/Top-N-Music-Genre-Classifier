import { useState } from 'react';
import {
  Container,
  Typography,
} from '@mui/material';
import { UploadButton } from '../components';

interface IResults {
  [key: string]: number
}

export const HomePage = () => {
  const [results, setResults] = useState<IResults>({});

  return (
    <Container>
      <Container sx={{ my: 2 }}>
        <Typography>
          Upload an audio file of at least 30s in length to see the genre prediction
          results.
        </Typography>
      </Container>
      <Container sx={{ mt: 2 }}>
        <UploadButton setResults={setResults}/>
      </Container>
      <Container sx={{ mt: 2 }}>
        {
          Object.keys(results).map((key, i) => {
            return (
              <div key={i}>{key}: {(100 * results[key]).toFixed(3)}%</div>
            );
          })
        }
      </Container>
    </Container>
  );
};
