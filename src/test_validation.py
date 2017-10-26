import unittest
from ddt import ddt, file_data

from validation import get_post_id_from_fb_url

expected_post_id = "10154885382271975"

@ddt
class ValidationTestCase(unittest.TestCase):
    
    @file_data('test_data_list.json')
    def test_post_id_match(self, test_url):

        post_id = get_post_id_from_fb_url(test_url)

        self.assertEqual(
                post_id,
                expected_post_id,
                'post_id {0} did not match expected id {1} '.format(post_id, expected_post_id))

if __name__ == '__main__':
        unittest.main(verbosity=2)

