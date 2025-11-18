import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Chip,
  Paper,
  Grid,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  ArrowBack,
  ThumbUp,
  Download,
  TrendingUp,
  CalendarToday,
  Code,
  Dataset,
} from '@mui/icons-material';
import { getModel } from '../services/api';

function ModelDetail() {
  const { modelId } = useParams();
  const navigate = useNavigate();
  const [model, setModel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadModel();
  }, [modelId]);

  const loadModel = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await getModel(decodeURIComponent(modelId));
      setModel(data);

      if (data.message) {
        setError(data.message);
      }
    } catch (err) {
      setError('Error loading model details. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 8 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="warning">{error}</Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/')}
          sx={{ mt: 2 }}
        >
          Back to Home
        </Button>
      </Container>
    );
  }

  if (!model || !model.id) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">Model not found</Alert>
        <Button
          startIcon={<ArrowBack />}
          onClick={() => navigate('/')}
          sx={{ mt: 2 }}
        >
          Back to Home
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate('/')}
        sx={{ mb: 2 }}
      >
        Back
      </Button>

      <Paper sx={{ p: 4 }}>
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            {model.id || model_id}
          </Typography>
          <Typography variant="h6" color="text.secondary" gutterBottom>
            by {model.author}
          </Typography>

          {/* Tags */}
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {model.pipeline_tag && (
              <Chip label={model.pipeline_tag} color="primary" />
            )}
            {model.library_name && (
              <Chip label={model.library_name} variant="outlined" />
            )}
            {model.license && (
              <Chip label={`License: ${model.license}`} variant="outlined" />
            )}
            {model.gated && <Chip label="Gated" color="warning" />}
          </Box>
        </Box>

        {/* Stats Grid */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {model.likes > 0 && (
            <Grid item xs={6} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <ThumbUp color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6">{model.likes.toLocaleString()}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Likes
                </Typography>
              </Box>
            </Grid>
          )}

          {model.downloads > 0 && (
            <Grid item xs={6} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Download color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6">{model.downloads.toLocaleString()}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Downloads
                </Typography>
              </Box>
            </Grid>
          )}

          {model.trending_score > 0 && (
            <Grid item xs={6} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <TrendingUp color="error" sx={{ fontSize: 40 }} />
                <Typography variant="h6">{model.trending_score}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Trending Score
                </Typography>
              </Box>
            </Grid>
          )}

          {model.derivative_count > 0 && (
            <Grid item xs={6} md={3}>
              <Box sx={{ textAlign: 'center' }}>
                <Code color="primary" sx={{ fontSize: 40 }} />
                <Typography variant="h6">{model.derivative_count}</Typography>
                <Typography variant="body2" color="text.secondary">
                  Derivatives
                </Typography>
              </Box>
            </Grid>
          )}
        </Grid>

        {/* Details */}
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Details
          </Typography>
          <Grid container spacing={2}>
            {model.created_at && (
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CalendarToday fontSize="small" />
                  <Typography variant="body2">
                    Created: {new Date(model.created_at).toLocaleDateString()}
                  </Typography>
                </Box>
              </Grid>
            )}
            {model.last_modified && (
              <Grid item xs={12} md={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <CalendarToday fontSize="small" />
                  <Typography variant="body2">
                    Updated: {new Date(model.last_modified).toLocaleDateString()}
                  </Typography>
                </Box>
              </Grid>
            )}
          </Grid>
        </Box>

        {/* Base Model */}
        {model.base_model && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Derived From
            </Typography>
            <Chip
              label={model.base_model}
              onClick={() => navigate(`/model/${encodeURIComponent(model.base_model)}`)}
              clickable
              color="secondary"
            />
          </Box>
        )}

        {/* Datasets */}
        {model.datasets && model.datasets.length > 0 && (
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Dataset />
              Training Datasets
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {model.datasets.map((dataset, idx) => (
                <Chip key={idx} label={dataset} variant="outlined" size="small" />
              ))}
            </Box>
          </Box>
        )}

        {/* HuggingFace Link */}
        <Button
          variant="contained"
          href={`https://huggingface.co/${model.id}`}
          target="_blank"
          rel="noopener noreferrer"
        >
          View on HuggingFace
        </Button>
      </Paper>
    </Container>
  );
}

export default ModelDetail;
