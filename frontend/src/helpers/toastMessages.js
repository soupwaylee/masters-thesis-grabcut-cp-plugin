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
  },
};

export {
  participantDataSubmission,
  submissionWarnings,
  scribbleSubmissionSuccess,
  segmentationSubmission
};