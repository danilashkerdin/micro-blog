from django.test import TestCase
from rest_framework.test import RequestsClient

SERVICE_NAME = 'likes/'
LOCALHOST = 'http://127.0.0.1:8000/'
GATEWAY = LOCALHOST + SERVICE_NAME


class LikesTestCase(TestCase):
    client = RequestsClient()

    def test_crete_likes(self):
        for userID in range(1, 10):
            name = "name" + str(userID)
            data = {'name': name, 'userID': userID, 'postID': userID}
            response = self.client.post(GATEWAY, data)

            self.assertTrue(response.status_code == 201)

    def test_get_likes(self):
        response = self.client.get(GATEWAY)
        assert response.status_code == 200

    def test_get_like_by_id(self):
        # getting
        self.test_crete_likes()
        for likeID in range(1, 10):
            response = self.client.get(GATEWAY + str(likeID) + '/')
            self.assertTrue(response.status_code == 200)
            self.assertTrue(response.json()['id'] == likeID)

    def test_delete_like_by_id(self):
        self.test_crete_likes()

        # deleting
        for likeID in range(1, 10):
            response = self.client.delete(GATEWAY + str(likeID) + '/')
            self.assertTrue(response.status_code == 204)

        # checking
        for likeID in range(1, 10):
            response = self.client.get(GATEWAY + str(likeID) + '/')
            self.assertTrue(response.status_code == 404)

    def test_put_like_by_id(self):
        self.test_crete_likes()

        # putting
        for likeID in range(1, 10):
            name = "name" + str(likeID + 10)
            data = {'name': name, 'userID': likeID + 10, 'postID': likeID + 10}
            response = self.client.put(GATEWAY + str(likeID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        # checking
        for likeID in range(1, 10):
            response = self.client.get(GATEWAY + str(likeID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['name'] == "name" + str(likeID + 10))
            self.assertTrue(data['userID'] == likeID + 10)

    def test_patch_like_by_id(self):
        self.test_crete_likes()

        for likeID in range(1, 10):
            data = {'name': 'new name'}
            response = self.client.patch(GATEWAY + str(likeID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        for likeID in range(1, 10):
            response = self.client.get(GATEWAY + str(likeID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['name'] == 'new name')

    def test_get_likes_by_post_id(self):
        self.test_crete_likes()

        for postID in range(1, 10):
            response = self.client.get(GATEWAY + '?postID=' + str(postID))
            assert response.status_code == 200
            pattern = [{'id': postID, 'postID': postID, 'userID': postID, 'name': 'name' + str(postID)}]
            self.assertEqual(response.json(), pattern)
