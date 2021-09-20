const participantDataSubmission = {
  success: {
    severity: 'success',
    summary: 'Thank you',
    detail: 'Received participant data',
    group: 'br',
    life: 4000,
  },
  error: {
  },
};

const submissionWarnings = {
  noForegroundScribbles: {
    severity: 'warn',
    summary: 'Annotations insufficient for segmentation',
    detail: `Please highlight a few definite-foreground pixels`,
    group: 'br',
    life: 4000,
  },
  noBackgroundScribbles: {
    severity: 'warn',
    summary: 'Annotations insufficient for segmentation',
    detail: `Please highlight a few definite-background pixels`,
    group: 'br',
    life: 4000,
  },
}

function scribbleSubmissionSuccess(scribbleCount) {
  const scribble_noun = scribbleCount > 1 ? 'scribbles' : 'scribble';
  return {
    severity: 'success',
    summary: 'Success',
    detail: `Computed segmentation from ${scribbleCount} ${scribble_noun}`,
    group: 'br',
    life: 3000,
  };
}

const segmentationSubmission = {
  success: {
    severity:'success',
    summary: 'Success',
    detail:'Received final segmentation choice',
    group: 'br',
    life: 4000,
  },
  error: {
    severity:'error',
    summary: 'Error',
    detail:'Oops, something went wrong - please re-submit',
    group: 'br',
    life: 5500,
  },
};

const fatalError = {
  severity:'error',
  summary: 'Oops',
  detail:'Sorry about that, this should not be happening - please refresh the page to re-start from the beginning.',
  group: 'br',
  life: 5500,
};

export {
  participantDataSubmission,
  submissionWarnings,
  scribbleSubmissionSuccess,
  segmentationSubmission,
  fatalError
};