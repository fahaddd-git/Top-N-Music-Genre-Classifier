import {
  AppBar,
  Container,
  Toolbar,
  Typography,
} from '@mui/material';
import MusicNote from '@mui/icons-material/MusicNoteSharp';

export const Header = () => (
  <AppBar
    color="primary"
    position="static"
  >
    <Container maxWidth="xl">
      <Toolbar disableGutters>
        <SiteName />
      </Toolbar>
    </Container>
  </AppBar>
);

const SiteName = () => (
  <>
    <MusicNote sx={{
      display: { xxs: 'none', md: 'flex' },
      mr: 1,
    }} />
    <Typography
      variant="overline"
      noWrap
    >
      Top-N Music Genre Classification Neural Network
    </Typography>
  </>
);
