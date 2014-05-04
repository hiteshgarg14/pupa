from pupa.scrape import Legislator, Committee, Person


def test_legislator_related_district():
    l = Legislator('John Adams', district='1')
    l.pre_save('jurisdiction-id')

    assert len(l._related) == 1
    assert l._related[0].person_id == l._id
    assert l._related[0].organization_id == 'legislature::jurisdiction-id'
    assert l._related[0].post_id == 'district::1'
    assert l._related[0].role == 'member'


def test_legislator_related_chamber_district():
    l = Legislator('John Adams', district='1', chamber='upper')
    l.pre_save('jurisdiction-id')

    assert len(l._related) == 1
    assert l._related[0].person_id == l._id
    assert l._related[0].organization_id == 'legislature:upper:jurisdiction-id'
    assert l._related[0].post_id == 'district:upper:1'
    assert l._related[0].role == 'member'


def test_legislator_related_party():
    l = Legislator('John Adams', district='1', party='Democratic-Republican')
    l.pre_save('jurisdiction-id')

    # a party membership
    assert len(l._related) == 2
    assert l._related[1].person_id == l._id
    assert l._related[1].organization_id == 'party:Democratic-Republican'
    assert l._related[1].role == 'member'


def test_committee_pre_save():
    # simplest case
    c = Committee('Defense')
    c.pre_save('jurisdiction-id')
    assert c.parent_id == 'legislature::jurisdiction-id'
    assert c.classification == 'committee'

    # with chamber
    c = Committee('Appropriations', chamber='upper')
    c.pre_save('jurisdiction-id')
    assert c.parent_id == 'legislature:upper:jurisdiction-id'

    # don't override set parent_id
    c2 = Committee('Farm Subsidies', parent_id=c._id)
    c2.pre_save('jurisdiction-id')
    assert c2.parent_id == c._id


def test_committee_add_member_person():
    c = Committee('Defense')
    p = Person('John Adams')
    c.add_member(p, role='chairman')
    assert c._related[0].person_id == p._id
    assert c._related[0].organization_id == c._id
    assert c._related[0].role == 'chairman'


def test_committee_add_member_name():
    c = Committee('Defense')
    c.add_member('John Adams')
    assert c._related[0].person_id == None
    assert c._related[0]._unmatched_legislator == {'name': 'John Adams'}
    assert c._related[0].organization_id == c._id
    assert c._related[0].role == 'member'