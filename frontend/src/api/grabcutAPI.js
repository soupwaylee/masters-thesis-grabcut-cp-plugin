import axios from 'axios';

const APIBaseURL = '/grabcut';

export class APIService {

  constructor() {
    this.instance = axios.create({
      baseURL: APIBaseURL,
      timeout: 1000 * 5,
    });
  }

  getDHMImage(imageID) {
    return this.instance.get(`/dhmimages/${imageID}`).then(response => response.data);
  }

  segmentImage(interactionRecord, scribbleContext) {
    const {scribbleIndices, scribbleTypes} = scribbleContext;

    return this.instance.post(
      '/gcsegmentation',
      {
        'interactionRecord': interactionRecord,
        'annotatedPixelIndices': scribbleIndices,
        'annotatedPixelTypes': scribbleTypes,
      }
    ).then(
      response => response.data
    );
  }
}