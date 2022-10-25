# Leaving Ethan's tests intact for now; these will be useful for API tests later

# class Upload(unittest.TestCase):
#     def test_upload_file(self):
#         f1 = "./tests/test_files/test.mp3"
#         files = {
#             "file": (f1, open(f1, "rb"), "audio/mpeg"),
#         }
#
#         response = client.post("/uploadfile", files=files)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertListEqual(list(dict.keys(response.json())), all_genres)
#
#     def test_upload_files(self):
#         f1 = "./tests/test_files/test.mp3"
#         f2 = "./tests/test_files/test.wav"
#         files = (
#             ("files", (f1, open(f1, "rb"), "audio/mpeg")),
#             ("files", (f2, open(f2, "rb"), "audio/wav")),
#         )
#
#         response = client.post("/uploadfiles", files=files)
#
#         self.assertEqual(response.status_code, 200)
#         self.assertListEqual(list(dict.keys(response.json())), [f1, f2])
