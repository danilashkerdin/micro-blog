from django.test import TestCase
from rest_framework.test import RequestsClient

SERVICE_NAME = 'posts/'
LOCALHOST = 'http://127.0.0.1:8000/'
GATEWAY = LOCALHOST + SERVICE_NAME


class PostsTestCase(TestCase):
    client = RequestsClient()

    def test_crete_posts(self):
        for userID in range(1, 10):
            text = "text" + str(userID)
            name = "name" + str(userID)
            data = {'text': text, 'name': name, 'userID': userID}
            response = self.client.post(GATEWAY, data)

            self.assertTrue(response.status_code == 201)

    def test_get_posts(self):
        response = self.client.get(GATEWAY)
        assert response.status_code == 200

    def test_get_post_by_id(self):

        self.test_crete_posts()
        for postID in range(1, 10):
            response = self.client.get(GATEWAY + str(postID) + '/')
            self.assertTrue(response.status_code == 200)
            self.assertTrue(response.json()['id'] == postID)

    def test_delete_post_by_id(self):
        self.test_crete_posts()
        for postID in range(1, 10):
            response = self.client.delete(GATEWAY + str(postID) + '/')
            self.assertTrue(response.status_code == 204)

        for postID in range(1, 10):
            response = self.client.get(GATEWAY + str(postID) + '/')
            self.assertTrue(response.status_code == 404)

    def test_put_post_by_id(self):
        self.test_crete_posts()

        for postID in range(1, 10):
            text = "text" + str(postID + 10)
            name = "name" + str(postID + 10)
            data = {'text': text, 'name': name, 'userID': postID + 10}
            response = self.client.put(GATEWAY + str(postID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        for postID in range(1, 10):
            response = self.client.get(GATEWAY + str(postID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['text'] == "text" + str(postID + 10))
            self.assertTrue(data['name'] == "name" + str(postID + 10))
            self.assertTrue(data['userID'] == postID + 10)

    def test_patch_post_by_id(self):
        self.test_crete_posts()

        for postID in range(1, 10):
            text = "text" + str(postID + 10)
            data = {'text': text}
            response = self.client.patch(GATEWAY + str(postID) + '/', data, content_type='application/json')
            self.assertTrue(response.status_code == 200)

        for postID in range(1, 10):
            response = self.client.get(GATEWAY + str(postID) + '/')
            self.assertTrue(response.status_code == 200)

            data = response.json()
            self.assertTrue(data['text'] == "text" + str(postID + 10))
