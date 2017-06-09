# -*- coding: utf-8 -*-
"""
Copyright 2017 Bernard Giroux, Elie Dumas-Lefebvre, Jerome Simon
email: Bernard.Giroux@ete.inrs.ca

This file is part of BhTomoPy.

BhTomoPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from borehole import Borehole
from mog import Mog, AirShots
from model import Model
from utils import Base


# Functions from 'database' require a module as first parameter. This
# is a way of allowing the coexistence of multiple instances of session
# throughout the program (one per module). Moreover, because the SQLAlchemy
# objects exist as attributes, they are permanent.


def create_data_management(module):
    """
    Initiate a module's SQLAlchemy attributes.
    """

    module.engine = create_engine("sqlite:///:memory:")  # 'engine' interacts with the file
    module.Session = sessionmaker(bind=module.engine)    # 'Session' acts as a factory for upcoming sessions; the features of 'Session' aren't exploited
    module.session = module.Session()                    # the objects are stored in 'session' and can be manipulated from there
    Base.metadata.create_all(module.engine)              # this creates the mapping for a specific engine
    module.modified = False                              # 'modified' keeps track of whether or not data has been modified since last save


def load(module, file):
    """
    Safely closes the current file opened in a module and opens a new file.
    """

    try:
        module.session.close()
        module.engine.dispose()

        module.engine = create_engine("sqlite:///" + file)
        module.Session = sessionmaker(bind=module.engine)
        module.session = module.Session()
        Base.metadata.create_all(module.engine)
        module.modified = False

        get_many(module)  # initiate the session's objects, guarantees they exist within 'session'

    except AttributeError:
        create_data_management(module)
        load(module, file)


def verify_mapping(module):
    """
    By referencing the items' relationships once, they don't get deleted by the closing of the
    current session (by the means of module.session.close() and module.engine.dispose()).
    """

    for item in module.session.query(Model).all():
        item.mogs, item.tt_covar
    for item in module.session.query(Mog).all():
        item.Tx, item.Rx, item.av, item.ap


def save_as(module, file):
    """
    Closes the current file, safely transfers its items to a new file and overwrites the selected file.
    To simply save a 'session' within the current file, the 'session.commit()' method is preferable.
    """

    try:
        strong_referencing = get_many(module)  # @UnusedVariable  # Guarantees the objects and their relationships survive the transfer
        verify_mapping(module)                                    # Referencing the attributes seems to guarantee the strong referencing's effectiveness
        items = get_many(module)  # temporarily stores the saved items

        module.session.close()
        module.engine.dispose()

        module.engine = create_engine("sqlite:///" + file)
        Base.metadata.create_all(module.engine)
        module.Session.configure(bind=module.engine)
        module.session = module.Session()

        for item in get_many(module):  # overwrites the selected file
            module.session.delete(item)

        items = [module.session.merge(item) for item in items]  # conforms the stored items to the new session
        module.session.add_all(items)

        module.session.commit()
        module.modified = False

    except AttributeError:
        create_data_management(module)
        save_as(module, file)


def get_many(module, *classes):
    """
    Get all or multiple classes stored within a session. Also guarantees these
    items are loaded into the session.
    """

    items = []

    if not classes:
        classes = (Borehole, Mog, AirShots, Model)

    for item in classes:

        items += module.session.query(item).all()

    return items


def delete(module, item):
    """
    Deletes an item, even if the item was just added (i.e. not committed, pending).
    """

    from sqlalchemy import inspect
    if inspect(item).persistent:
        module.session.delete(item)
    else:
        module.session.expunge(item)
    module.modified = True


def airshots_cleanup(module):
    pass


def long_url(module):
    return str(module.engine.url)[10:]


def short_url(module):
    return os.path.basename(long_url(module))


if __name__ == '__main__':

    import sys
    current_module = sys.modules[__name__]
    create_data_management(current_module)

    current_module.session.add(Borehole('test3'))
    current_module.session.add(Borehole('test1'))
    current_module.session.flush()
    current_module.session.add(Borehole('test2'))

    from sqlalchemy import inspect
    for item in current_module.session.query(Borehole).all():
        print(item.name, inspect(item).persistent)


# Gets the current module, so that it can be sent as a parameter.
# import sys
# current_module = sys.modules[__name__]


#         from sqlalchemy.orm.attributes import flag_modified
#         flag_modified(module.session.query(Model).all()[0], 'tt_covar')


# Test bank
#                     from sqlalchemy import inspect
#                     from sqlalchemy.engine import reflection
#                     from sqlalchemy.orm.session import sessionmaker
#                     print(reflection.Inspector.from_engine(database.engine).get_table_names())
#                     print(items)
#                     print([i.__tablename__ for i in items])
#                     print(reflection.Inspector.from_engine(database.session.get_bind()).get_table_names())
#                     print([sessionmaker.object_session(i) for i in items])
#                     print(database.session)
#                     print([sessionmaker.object_session(i) for i in items])
#                     print(reflection.Inspector.from_engine(database.session.get_bind()).get_table_names())
#                     print([i.__tablename__ for i in items])
#                     print(database.session.get_bind().url)
#                     print([inspect(my_object) for my_object in items])
#                     database.session.commit()
#                     print([inspect(my_object).persistent for my_object in items])
#                     print([i.__tablename__ for i in database.session])
#                     print(database.session.query(Borehole).all())
