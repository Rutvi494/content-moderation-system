import "./App.css";

import ImageUploader
  from "./components/ImageUploader";


function App() {
  return (
    <div className="app">

      <header className="app-header">

        <div>
          <p className="eyebrow">
            AWS + AI PROJECT
          </p>

          <h1>
            Design a Content Moderation
            System Using AI
          </h1>

          <p className="subtitle">
            Upload an image and analyze it
            using Amazon Rekognition.
          </p>
        </div>

      </header>

      <main>
        <ImageUploader />
      </main>

    </div>
  );
}


export default App;
