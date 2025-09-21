import React, { useState, useEffect } from 'react';

export default function Spotify() {
  const [loginStatus, setLoginStatus] = useState('ready'); 
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    // Check for Spotify return parameters
    const urlParams = new URLSearchParams(window.location.search);
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    
    const authCode = urlParams.get('code') || hashParams.get('code');
    const error = urlParams.get('error') || hashParams.get('error');
    const state = urlParams.get('state') || hashParams.get('state');
    
    const hasSpotifyParams = authCode || error || state;
    
    if (hasSpotifyParams && loginStatus === 'ready') {
      console.log('🎵 User returned from Spotify! Auto-running script...');
      
      // Clean up URL
      window.history.replaceState({}, document.title, window.location.pathname);
      
      // SILENTLY run the script
      setLoginStatus('running');
      
      // Auto-trigger script
      setTimeout(() => {
        runMusicScript();
      }, 1000);
    }
  }, [loginStatus]);

  const runMusicScript = async () => {
    try {
      // Call our server to run the script SILENTLY
      const response = await fetch('http://localhost:5001/run-music-script', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      const result = await response.json();
      
      if (result.success) {
        // Start polling for results SILENTLY
        pollForDataFile();
      } else {
        setLoginStatus('ready');
      }
      
    } catch (error) {
      setLoginStatus('ready');
    }
  };

  const pollForDataFile = () => {
    let attempts = 0;
    const maxAttempts = 60;
    
    const checkForData = setInterval(async () => {
      attempts++;
      try {
        const timestamp = Date.now();
        const response = await fetch(`./data.js?v=${timestamp}`);
        
        if (response.ok) {
          const text = await response.text();
          
          if (text.includes('const articles')) {
            clearInterval(checkForData);
            
            const articlesMatch = text.match(/const articles = (\[.*?\]);/s);
            if (articlesMatch) {
              const articlesData = JSON.parse(articlesMatch[1]);
              setArticles(articlesData);
              setLoginStatus('complete');
              console.log(`🎉 Success! Found ${articlesData.length} personalized articles!`);
            }
          }
        }
      } catch (error) {
        // Silent
      }
      
      if (attempts >= maxAttempts) {
        clearInterval(checkForData);
        setLoginStatus('ready');
      }
    }, 2000);
  };

  const handleSpotifyLogin = () => {
    // Just let the link work - NO STATUS CHANGES
  };

  return (
    <div className="spotify-container">
      <a 
        href='http://localhost:8888' 
        className="spotify-login-btn"
        onClick={handleSpotifyLogin}
      >
        <span className="spotify-icon">🎵</span>
        Login to Spotify
      </a>
      
      {/* NO POPUPS, NO MESSAGES, NOTHING */}
    </div>
  );
}