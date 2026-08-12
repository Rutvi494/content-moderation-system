import { useEffect, useState } from "react";

import {
  getPresignedUploadUrl,
  uploadImageToS3,
  moderateImage,
} from "../services/moderationApi";

import ModerationResult from "./ModerationResult";


const ALLOWED_TYPES = [
  "image/jpeg",
  "image/png",
];

const MAX_FILE_SIZE = 5 * 1024 * 1024;


function ImageUploader() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] =
    useState(null);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [status, setStatus] =
    useState("");


  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(
          previewUrl
        );
      }
    };
  }, [previewUrl]);


  function handleFileChange(event) {
    const selectedFile =
      event.target.files?.[0];

    setError("");
    setResult(null);
    setStatus("");

    if (!selectedFile) {
      setFile(null);
      setPreviewUrl(null);

      return;
    }

    if (
      !ALLOWED_TYPES.includes(
        selectedFile.type
      )
    ) {
      setError(
        "Only JPEG and PNG images are supported."
      );

      event.target.value = "";

      return;
    }

    if (
      selectedFile.size >
      MAX_FILE_SIZE
    ) {
      setError(
        "Image must be 5 MB or smaller."
      );

      event.target.value = "";

      return;
    }

    if (previewUrl) {
      URL.revokeObjectURL(
        previewUrl
      );
    }

    setFile(selectedFile);

    setPreviewUrl(
      URL.createObjectURL(
        selectedFile
      )
    );
  }


  async function handleModeration() {
    if (!file) {
      setError(
        "Please select an image first."
      );

      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      setStatus(
        "Creating secure upload URL..."
      );

      const {
        upload_url,
        object_key,
      } =
        await getPresignedUploadUrl(
          file
        );

      setStatus(
        "Uploading image to Amazon S3..."
      );

      await uploadImageToS3(
        upload_url,
        file
      );

      setStatus(
        "Analyzing image with AI..."
      );

      const moderationResult =
        await moderateImage(
          object_key
        );

      setResult(
        moderationResult
      );

      setStatus(
        "Moderation complete."
      );
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Something went wrong."
      );

      setStatus("");
    } finally {
      setLoading(false);
    }
  }


  function handleReset() {
    if (previewUrl) {
      URL.revokeObjectURL(
        previewUrl
      );
    }

    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError("");
    setStatus("");

    const input =
      document.getElementById(
        "image-input"
      );

    if (input) {
      input.value = "";
    }
  }


  return (
    <div className="moderation-container">

      <div className="upload-card">

        <h2>
          Upload Image
        </h2>

        <p className="description">
          Upload a JPEG or PNG image
          to analyze it for potentially
          unsafe content.
        </p>

        <label
          className="file-input-label"
          htmlFor="image-input"
        >
          Choose Image
        </label>

        <input
          id="image-input"
          className="file-input"
          type="file"
          accept="image/jpeg,image/png"
          onChange={handleFileChange}
        />

        {file && (
          <div className="file-details">

            <strong>
              {file.name}
            </strong>

            <span>
              {(
                file.size /
                1024 /
                1024
              ).toFixed(2)}
              {" MB"}
            </span>

          </div>
        )}

        {previewUrl && (
          <div className="preview-container">

            <img
              src={previewUrl}
              alt="Selected content preview"
              className="image-preview"
            />

          </div>
        )}

        <div className="button-group">

          <button
            className="primary-button"
            onClick={
              handleModeration
            }
            disabled={
              !file || loading
            }
          >
            {loading
              ? "Processing..."
              : "Moderate Image"}
          </button>

          {file && (
            <button
              className="secondary-button"
              onClick={
                handleReset
              }
              disabled={loading}
            >
              Reset
            </button>
          )}

        </div>

        {status && (
          <div className="status-message">
            {status}
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

      </div>

      <ModerationResult
        result={result}
      />

    </div>
  );
}


export default ImageUploader;