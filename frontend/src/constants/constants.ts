 /* eslint-disable */

export default Object.freeze({
  SUMMARY_TYPES: {
    PER_RUN: 'per_run',
    DAILY: 'daily',
    WEEKLY: 'weekly'
  },
  API_BASE_PATH: process.env.NODE_ENV === 'development' ? 'http://localhost:9005' : ''
})
