## Top N Music Genre Classifier

### Description
A music genre classifier

### Deployment Instructions


### Making Contributions



### Project Structure
#### Frontend
Houses the web frontend.\
Built with [React](https://reactjs.org/) and [MUI](https://mui.com/).

#### Services
##### etl-service
Contains the ETL data pipeline.

##### neural-network
Contains the model-generating convolutional neural network

##### prediction-api
Contains the API that provides an interface between the web frontend and the generated model.\
Built with [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/).

##### utilities
Contains shared program logic
