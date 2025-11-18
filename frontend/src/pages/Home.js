import React, { useState, useEffect } from 'react';
import {
  Container,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Search as SearchIcon, TrendingUp, Download, ThumbUp } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { searchModels, getTrending, getStats } from '../services/api';

function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [trending, setTrending] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [trendingData, statsData] = await Promise.all([
        getTrending(10),
        getStats(),
      ]);
      setTrending(trendingData.models || []);
      setStats(statsData);
    } catch (err) {
      console.error('Error loading initial data:', err);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const results = await searchModels({ q: searchQuery, per_page: 20 });
      setSearchResults(results.results || []);

      if (results.message) {
        setError(results.message);
      }
    } catch (err) {
      setError('Error searching models. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const ModelCard = ({ model }) => (
    <Card
      sx={{ height: '100%', cursor: 'pointer', '&:hover': { boxShadow: 6 } }}
      onClick={() => navigate(`/model/${encodeURIComponent(model.id || model.model_id)}`)}
    >
      <CardContent>
        <Typography variant="h6" component="div" noWrap>
          {model.id || model.model_id}
        </Typography>
        <Typography color="text.secondary" gutterBottom>
          by {model.author}
        </Typography>

        {model.pipeline_tag && (
          <Chip
            label={model.pipeline_tag}
            size="small"
            color="primary"
            sx={{ mr: 1, mb: 1 }}
          />
        )}

        <Box sx={{ display: 'flex', gap: 2, mt: 2, flexWrap: 'wrap' }}>
          {model.likes > 0 && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <ThumbUp fontSize="small" />
              <Typography variant="body2">{model.likes.toLocaleString()}</Typography>
            </Box>
          )}
          {model.downloads > 0 && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <Download fontSize="small" />
              <Typography variant="body2">{model.downloads.toLocaleString()}</Typography>
            </Box>
          )}
          {model.trending_score > 0 && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <TrendingUp fontSize="small" color="error" />
              <Typography variant="body2">{model.trending_score}</Typography>
            </Box>
          )}
        </Box>

        {model.derivative_count > 0 && (
          <Typography variant="caption" display="block" sx={{ mt: 1 }}>
            {model.derivative_count} derivatives
          </Typography>
        )}
      </CardContent>
    </Card>
  );

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Discover AI Models
        </Typography>
        <Typography variant="h6" color="text.secondary" gutterBottom>
          Search, explore, and analyze 331,992+ AI models from HuggingFace
        </Typography>

        {stats && (
          <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center', gap: 3, flexWrap: 'wrap' }}>
            <Chip label={`${stats.total_models?.toLocaleString() || '331K+'} Models`} color="primary" />
            <Chip label={`${stats.pipeline_types ? Object.keys(stats.pipeline_types).length : '30+'} Categories`} />
            <Chip label={`${stats.languages_supported || '184+'} Languages`} />
          </Box>
        )}
      </Box>

      {/* Search Bar */}
      <Box component="form" onSubmit={handleSearch} sx={{ mb: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={10}>
            <TextField
              fullWidth
              placeholder="Search models (e.g., 'llama text-generation', 'image classification', 'ocr')"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              variant="outlined"
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="contained"
              type="submit"
              startIcon={<SearchIcon />}
              sx={{ height: '56px' }}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Search'}
            </Button>
          </Grid>
        </Grid>
      </Box>

      {/* Error Message */}
      {error && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Search Results */}
      {searchResults.length > 0 && (
        <Box sx={{ mb: 6 }}>
          <Typography variant="h5" gutterBottom>
            Search Results ({searchResults.length})
          </Typography>
          <Grid container spacing={3}>
            {searchResults.map((model) => (
              <Grid item xs={12} sm={6} md={4} key={model.id}>
                <ModelCard model={model} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Trending Section */}
      {trending.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUp color="error" />
            Trending Now
          </Typography>
          <Grid container spacing={3}>
            {trending.map((model) => (
              <Grid item xs={12} sm={6} md={4} key={model.id || model.model_id}>
                <ModelCard model={model} />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Empty State */}
      {!loading && searchResults.length === 0 && trending.length === 0 && !error && (
        <Box sx={{ textAlign: 'center', mt: 8 }}>
          <Typography variant="h6" color="text.secondary">
            Search for models or browse trending models above
          </Typography>
        </Box>
      )}
    </Container>
  );
}

export default Home;
