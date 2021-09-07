import axios from 'axios';

const APIBaseURL = '/grabcut';

export class APIService {

  constructor() {
    this.instance = axios.create({
      baseURL: APIBaseURL,
      timeout: 1000 * 9,
    });
  }

  submitParticipantData(sessionId, ageGroup, academicField) {
    return this.instance.post(
      '/demographics/',
      {
        'sessionId': sessionId,
        'ageGroup': ageGroup,
        'academicField': academicField,
      }
    ).then(
      response => response.data
    );
  }

  getDHMImage(imageID) {
    return this.instance.get(`/dhmimages/${imageID}`).then(response => response.data);
  }

  segmentImage(interactionRecord, scribbleContext) {
    const {scribbleIndices, scribbleTypes} = scribbleContext;

    return this.instance.post(
      '/gcsegmentation/',
      {
        'interactionRecord': interactionRecord,
        'annotatedPixelIndices': scribbleIndices,
        'annotatedPixelTypes': scribbleTypes,
      }
    ).then(
      response => response.data
    );
  }

  submitSegmentation(sessionId, imageId, interactionRecordId, segmentationMask) {
    return this.instance.post(
      '/masks/',
      {
        'sessionId': sessionId,
        'imageId': imageId,
        'interactionRecordId': interactionRecordId,
        'mask': segmentationMask,
      }
    ).then(
      response => response.data
    );
  }
}