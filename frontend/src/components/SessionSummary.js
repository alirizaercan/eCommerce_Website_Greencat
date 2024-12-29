import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getSessionById } from '../services/sessionApi';
import '../styles/SessionSummary.css';
import { useParams } from 'react-router-dom';

const SessionSummary = ({ sessionId }) => {
  const [session, setSession] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSession = async () => {
      if (!sessionId) {
        setError('Oturum ID gereklidir');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await getSessionById(sessionId);
        if (data) {
          setSession(data);
        } else {
          setError('Oturum bilgileri yüklenemedi');
        }
      } catch (err) {
        setError('Oturum yüklenirken hata oluştu');
        console.error('Oturum yükleme hatası:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchSession();
  }, [sessionId]);

  if (loading) {
    return <div className="session-summary loading">Oturum detayları yükleniyor...</div>;
  }

  if (error) {
    return <div className="session-summary error">
      <p className="error-message">{error}</p>
    </div>;
  }

  if (!session) {
    return <div className="session-summary not-found">
      <p>Oturum bilgisi bulunamadı</p>
    </div>;
  }

  return (
    <div className="session-summary">
      <h2>Oturum Detayları</h2>
      <div className="session-info">
        <div className="info-item">
          <span className="label">Oturum No:</span>
          <span className="value">{session.session_id}</span>
        </div>
        <div className="info-item">
          <span className="label">Müşteri:</span>
          <span className="value">{session.customer_id}</span>
        </div>
        <div className="info-item">
          <span className="label">Toplam:</span>
          <span className="value">{Number(session.total).toLocaleString('tr-TR', {
            style: 'currency',
            currency: 'TRY'
          })}</span>
        </div>
      </div>
    </div>
  );
};

SessionSummary.propTypes = {
  sessionId: PropTypes.number.isRequired
};

export default SessionSummary;