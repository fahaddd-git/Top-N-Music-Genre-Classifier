import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#0c3c58',
    },
    secondary: {
      main: '#247b77',
    },
  },
  typography: {
    overline: {
      fontWeight: 400,
      fontSize: '0.7rem',
      lineHeight: 2.6,
      letterSpacing: '0.15em',
    },
  },
});
