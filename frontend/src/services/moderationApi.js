const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured."
  );
}


export async function getPresignedUploadUrl(file) {
  const response = await fetch(
    `${API_BASE_URL}/uploads/presigned-url`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        file_name: file.name,
        content_type: file.type,
      }),
    }
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      error || "Failed to create upload URL."
    );
  }

  return response.json();
}


export async function uploadImageToS3(
  uploadUrl,
  file
) {
  const response = await fetch(
    uploadUrl,
    {
      method: "PUT",
      headers: {
        "Content-Type": file.type,
      },
      body: file,
    }
  );

  if (!response.ok) {
    throw new Error(
      "Image upload to S3 failed."
    );
  }
}


export async function moderateImage(
  objectKey,
  userId = "user-101"
) {
  const response = await fetch(
    `${API_BASE_URL}/moderation/image`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        object_key: objectKey,
      }),
    }
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      error || "Image moderation failed."
    );
  }

  return response.json();
}


async function readError(response) {
  try {
    const data = await response.json();

    return data.message;
  } catch {
    return null;
  }
}