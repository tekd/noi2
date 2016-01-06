from .test_models import DbTestCase
from .factories import UserFactory

from app import noi1
from app.models import db, Noi1MigrationInfo

SAMPLE_USER = {
    "city": "", 
    "first_name": "Foo", 
    "last_name": "Bar", 
    "domain_expertise": None, 
    "picture": "https://pbs.twimg.com/profile_images/123123_normal.jpeg", 
    "title": "Project Manager", 
    "skills": {
        "opendata/implementing-an-open-data-program/making-machine-readable": "1", 
        "opendata/implementing-an-open-data-program/open-data-standards": "1", 
        "opendata/implementing-an-open-data-program/open-data-formats": "-1",
    },
    "country": "United States", 
    "latlng": "(41.123, -72.123)", 
    "userid": "twitter:123123123", 
    "org_type": "org", 
    "country_code": "US", 
    "timestamp": "2015-06-03T19:47:30.057746", 
    "domains": [], 
    "org": "FooOrg", 
    "langs": [
        "English"
    ], 
    "email": u"foo@example.org", 
    "projects": None
}

class Noi1MigrationInfoTests(DbTestCase):
    def test_is_none_by_default(self):
        user = UserFactory.create(email=u'foo@example.org', password='foo')
        db.session.commit()
        self.assertEqual(user.noi1_migration_info, None)

    def test_is_added_on_import(self):
        user = noi1.add_user_to_db(SAMPLE_USER, password='foo')
        db.session.commit()
        self.assertEqual(user.noi1_migration_info.noi1_userid,
                         'twitter:123123123')

    def test_is_deleted_along_with_user(self):
        user = noi1.add_user_to_db(SAMPLE_USER, password='foo')
        db.session.commit()
        db.session.delete(user)
        db.session.commit()

        query = Noi1MigrationInfo.query.filter(
            Noi1MigrationInfo.noi1_userid == 'twitter:123123123'
        )
        self.assertEqual(len(query.all()), 0)