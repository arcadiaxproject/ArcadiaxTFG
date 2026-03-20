import React, { useState, useEffect, useRef } from 'react';

const styles = {
  root: {
    margin: 0,
    padding: 0,
    width: '100vw',
    height: '100vh',
    background: '#000',
    overflow: 'hidden',
    fontFamily: "'Segoe UI', Arial, sans-serif",
    color: '#fff',
  },
  idle: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '100%',
    background: '#000',
  },
  logo: {
    fontSize: '5rem',
    fontWeight: '700',
    letterSpacing: '0.2em',
    color: '#fff',
    textTransform: 'uppercase',
    opacity: 0.9,
  },
  logoAccent: {
    color: '#e63946',
  },
  tagline: {
    marginTop: '1rem',
    fontSize: '1rem',
    letterSpacing: '0.4em',
    color: '#888',
    textTransform: 'uppercase',
  },
  videoWrapper: {
    position: 'relative',
    width: '100%',
    height: '100%',
    background: '#000',
  },
  video: {
    width: '100%',
    height: '100%',
    objectFit: 'contain',
    display: 'block',
    background: '#000',
  },
  overlay: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: '1.5rem 2rem',
    background: 'linear-gradient(transparent, rgba(0,0,0,0.85))',
    pointerEvents: 'none',
  },
  overlayTitle: {
    fontSize: '1.8rem',
    fontWeight: '600',
    margin: 0,
    letterSpacing: '0.05em',
  },
  overlayMeta: {
    fontSize: '0.9rem',
    color: '#aaa',
    marginTop: '0.3rem',
    letterSpacing: '0.1em',
    textTransform: 'uppercase',
  },
  stopButton: {
    position: 'absolute',
    top: '1rem',
    right: '1rem',
    background: 'rgba(0,0,0,0.6)',
    border: '1px solid rgba(255,255,255,0.3)',
    color: '#fff',
    padding: '0.4rem 0.9rem',
    borderRadius: '4px',
    fontSize: '0.8rem',
    cursor: 'pointer',
    letterSpacing: '0.08em',
    textTransform: 'uppercase',
  },
};

export default function App() {
  const [state, setState] = useState({
    playing: false,
    videoPath: null,
    title: null,
    type: null,
    consoleName: null,
  });

  const videoRef = useRef(null);

  const stopPlayback = () => {
    setState({ playing: false, videoPath: null, title: null, type: null, consoleName: null });
    if (videoRef.current) {
      videoRef.current.pause();
      videoRef.current.src = '';
    }
  };

  const handleStopButton = () => {
    fetch('http://localhost:8000/playback/stop', { method: 'POST' }).catch(() => {});
    stopPlayback();
  };

  useEffect(() => {
    if (!window.arcadia) return;

    window.arcadia.onPlayVideo((data) => {
      const src = data.path;

      setState({
        playing: true,
        videoPath: src,
        title: data.title || null,
        type: data.type || null,
        consoleName: data.console || null,
      });
    });

    window.arcadia.onStopVideo(() => {
      stopPlayback();
    });
  }, []);

  useEffect(() => {
    if (state.playing && videoRef.current && state.videoPath) {
      videoRef.current.src = state.videoPath;
      videoRef.current.load();
      videoRef.current.play().catch((err) => {
        console.error('[Video] Playback error:', err);
      });
    }
  }, [state.playing, state.videoPath]);

  if (!state.playing) {
    return (
      <div style={styles.idle}>
        <div style={styles.logo}>
          Arcadia<span style={styles.logoAccent}>X</span>
        </div>
        <div style={styles.tagline}>Insert Coin to Play</div>
      </div>
    );
  }

  const metaLabel =
    state.type === 'game' && state.consoleName
      ? state.consoleName.toUpperCase()
      : state.type === 'film'
      ? 'FILM'
      : '';

  return (
    <div style={styles.videoWrapper}>
      <video
        ref={videoRef}
        style={styles.video}
        autoPlay
        controls={false}
        onEnded={handleStopButton}
      />

      <div style={styles.overlay}>
        {state.title && <p style={styles.overlayTitle}>{state.title}</p>}
        {metaLabel && <p style={styles.overlayMeta}>{metaLabel}</p>}
      </div>

      <button style={styles.stopButton} onClick={handleStopButton}>
        Stop
      </button>
    </div>
  );
}
