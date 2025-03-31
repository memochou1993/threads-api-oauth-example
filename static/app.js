const THREADS_APP_ID = '9030817430362187';
const THREADS_AUTH_URL = 'https://threads.net/oauth/authorize';

const messageElement = document.getElementById('message');
const accessTokenElement = document.getElementById('access-token');
const longLivedAccessTokenElement = document.getElementById('long-lived-access-token');

const getAccessToken = () => {
  const url = new URL(THREADS_AUTH_URL);

  url.search = new URLSearchParams({
    client_id: THREADS_APP_ID,
    redirect_uri: `${window.location.origin}/auth/callback`,
    scope: 'threads_basic,threads_content_publish',
    response_type: 'code',
  }).toString();

  window.location.href = url.toString();
};

const getLongLivedAccessToken = async () => {
  messageElement.innerText = 'Retrieving long-lived access token...';
  try {
    const response = await fetch(`/long-lived-access-token?access_token=${accessTokenElement.innerText}`);
    const data = await response.json();
    if (data.access_token) {
      longLivedAccessTokenElement.innerText = data.access_token;
    }
    messageElement.innerText = data.detail || 'Retrieved long-lived access token successfully!';
  } catch (error) {
    messageElement.innerText = error.message;
  }
};

window.onload = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const code = urlParams.get('code');
  if (code) {
    messageElement.innerText = 'Retrieving access token...';
    try {
      const response = await fetch('/access-token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          redirect_uri: `${window.location.origin}/auth/callback`,
        }),
      });
      const data = await response.json();
      if (data.access_token) {
        accessTokenElement.innerText = data.access_token;
      }
      messageElement.innerText = data.detail || 'Retrieved access token successfully!';
    } catch (error) {
      messageElement.innerText = error.message;
    }
  }
};
