import unittest
from app import create_app
from db import db


class GCInteractionRecordTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(config="testing")
        self.client = self.app.test_client
        self.interaction_record = {
            'session_id': 'session1',
            'image_id': 1,
            'annotated_pixels': 100
        }

        with self.app.app_context():
            db.create_all()

    def tearDownClass(self) -> None:
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def should_returnpersistentrecord_when_postwithrecord(self):
        res = self.client().post('/graphcuts/', data=self.interaction_record)
        self.assertEqual(res.status_code, 201)
        self.assertIn('session1', str(res.data))


if __name__ == "__main__":
    unittest.main()
