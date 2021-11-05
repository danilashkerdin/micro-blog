from django.test import TestCase
from rest_framework.test import RequestsClient

SERVICE_NAME = 'comments/'
LOCALHOST = 'http://127.0.0.1:8000/'
GATEWAY = LOCALHOST + SERVICE_NAME


class CommentsTestCase(TestCase):
    client = RequestsClient()

    def test_crete_comments(self):
        for userID in range(1, 10):
            name = "name" + str(userID)
            data = {'name': name, 'userID': userID, 'postID': userID, 'text': name}
            response = self.client.post(GATEWAY, data)

            self.assertTrue(response.status_code == 201)

    def test_get_comments(self):
        response = self.client.get(GATEWAY)
        assert response.status_code == 200

    def test_get_comments_by_id(self):
        # getting
        self.test_crete_comments()
        for commentID in range(1, 10):
            response = self.client.get(GATEWAY + str(commentID) + '/')
            self.assertTrue(response.status_code == 200)
            self.assertTrue(response.json()['id'] == commentID)

    def test_delete_comment_by_id(self):
        self.test_crete_comments()

        # deleting
        for commentID in range(1, 10):
            response = self.client.delete(GATEWAY + str(commentID) + '/')
            self.assertTrue(response.status_code == 204)

        # checking
        for commentID in range(1, 10):
            response = self.client.get(GATEWAY + str(commentID) + '/')
            self.assertTrue(response.status_code == 404)

    def test_put_comment_by_id(self):
        self.test_crete_comments()

        # putting
        for commentID in range(1, 10):
            name = "name" + str(commentID + 10)
            userID = commentID + 10
            postID = commentID + 10
            text = 'new text'
            data = {'name': name, 'userID': userID, 'postID': postID, 'text': text}
            response = self.client.put(GATEWAY + str(commentID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        # checking
        for commentID in range(1, 10):
            response = self.client.get(GATEWAY + str(commentID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['name'] == "name" + str(commentID + 10))
            self.assertTrue(data['userID'] == commentID + 10)
            self.assertTrue(data['postID'] == commentID + 10)
            self.assertTrue(data['text'] == 'new text')

    def test_patch_comment_by_id(self):
        self.test_crete_comments()

        for commentID in range(1, 10):
            data = {'name': 'new name'}
            response = self.client.patch(GATEWAY + str(commentID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        for commentID in range(1, 10):
            response = self.client.get(GATEWAY + str(commentID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['name'] == 'new name')

    def test_get_comments_by_post_id(self):
        self.test_crete_comments()

        for postID in range(1, 10):
            response = self.client.get(GATEWAY + '?postID=' + str(postID))
            assert response.status_code == 200
            pattern = [{'id': postID, 'userID': postID, 'postID': postID, 'text': 'name' + str(postID),
                        'name': 'name' + str(postID)}]
            self.assertEqual(response.json(), pattern)
