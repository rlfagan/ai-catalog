import React from 'react';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, cursor: 'pointer' }}
            onClick={() => navigate('/')}
          >
            🤖 AI Model Catalog
          </Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            331K+ Models
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Header;
