export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status?: number,
    public readonly code?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function handleApiError(error: unknown, defaultMessage: string): never {
  if (error instanceof ApiError) {
    throw error;
  }

  if (error instanceof Error) {
    throw new ApiError(error.message);
  }

  throw new ApiError(defaultMessage);
}