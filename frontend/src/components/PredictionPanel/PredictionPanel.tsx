import { useState } from 'react';
import {
  Alert,
  AlertTitle,
  Collapse,
  Container,
  TableContainer,
  Typography,
} from '@mui/material';
import { UploadButton } from 'src/components';
import { useGetPredictions } from './hooks';
import { PredictionTable } from './PredictionTable';

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
      <Container sx={{ my: 2 }}>
        <Typography variant="h6">
          Upload
        </Typography>
        <UploadButton
          onChange={onChange}
          loading={loading}
        />
      </Container>
      { error && <ErrorAlert error={error} /> }
      <Container sx={{ mt: 3 }}>
        { predictions !== null && (
          <>
            <Typography variant="h6">
              Predictions
            </Typography>
            <TableContainer>
              <PredictionTable
                columns={[
                  'Genre',
                  'Confidence',
                ]}
                predictions={predictions}
              />
            </TableContainer>
          </>
        )}
      </Container>
    </>
  );
};

/**
 * Dismissable error toast. Adapted from:
 *  URL: https://mui.com/material-ui/react-alert/#actions &
 *       https://mui.com/material-ui/react-alert/#transition
 *  Date: 11/15/22
 */
const ErrorAlert = ({ error }: { error: string }) => {
  const [open, setOpen] = useState(true);
  return (
    <Collapse in={open}>
      <Container maxWidth="xs" sx={{ float: 'left' }}>
        <Alert severity="error" onClose={() => setOpen(false)}>
          <AlertTitle>Error</AlertTitle>
          { error }
        </Alert>
      </Container>
    </Collapse>
  );
};
