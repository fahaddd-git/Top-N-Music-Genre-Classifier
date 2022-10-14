
"""

IANA is the official registry of MIME media types and maintains a list of all
the official MIME types. The url is here:

https://www.iana.org/assignments/media-types/media-types.xhtml

Of course some of these audio formats here are obscure and are likely not
processable by librosa or tensorflow. For now I will list some common ones.

Also see
https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types

"""

content_type_audio = set((
    "audio/mpeg",
    "audio/oog",
    "audio/wav",
))
