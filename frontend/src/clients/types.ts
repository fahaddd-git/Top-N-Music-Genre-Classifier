export type FastAPIValidationErrorResponse = { detail: ValidationErrorDetail[] };
export type FastAPIClientErrorResponse = { detail: string };

type ValidationErrorDetail = {
  loc: string[];
  msg: string;
  type: string;
};

export function isFastAPIValidationErrorResponse (
  object: any
): object is FastAPIValidationErrorResponse {
  return Array.isArray(object?.detail) && object?.detail?.msg !== undefined;
}

export function isFastAPIClientErrorResponse (
  object: any
): object is FastAPIClientErrorResponse {
  return typeof (object?.detail) === 'string';
}
