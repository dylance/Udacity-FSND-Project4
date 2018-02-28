from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Items, User


engine = create_engine('sqlite:///db-with-user.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Add original user

User1 = User(name="Dylan Ellison", email="dylancellison@gmail.com",
             picture=("https://avatars2.githubusercontent.com/u/17778111"
                      "?s=400&u=dccdea06297fbb8f57c6e37b0d36ab83eedec2db&v=4"))

session.add(User1)
session.commit()

# Category for Snowboarding
category1 = Categories(user_id=1,
                       category="Snowboarding",
                       description="extreme downhill sport on snow")

session.add(category1)
session.commit()


Item1 = Items(user_id=1,
              item="Burton Custom",
              description="all terrain freestyle board",
              category=category1)

session.add(Item1)
session.commit()

Item2 = Items(user_id=1,
              item="Burton Vapor",
              description="The only board Erik Brown will ride",
              category=category1)

session.add(Item2)
session.commit()

Item3 = Items(user_id=1,
              item="Lobster snowboard",
              description="Haldor jibs on this",
              category=category1)

session.add(Item3)
session.commit()

# cateogory for surfing
category2 = Categories(user_id=1,
                       category="Surfing",
                       description="Riding ocean waves")

session.add(category2)
session.commit()


Item1 = Items(user_id=1,
              item="Al Merrick flyer",
              description="good all around board",
              category=category2)

session.add(Item1)
session.commit()

Item2 = Items(user_id=1,
              item="Costco Wavestorm",
              description="the best board out there.",
              category=category2)

session.add(Item2)
session.commit()

Item3 = Items(user_id=1,
              item="lost round nose fish",
              description="everyone needs this in their quiver",
              category=category2)

session.add(Item3)
session.commit()


# category for skateboarding
category3 = Categories(user_id=1,
                       category="Skateboarding",
                       description="surfing on concrete")

session.add(category3)
session.commit()


Item1 = Items(user_id=1,
              item="Tom Penny board",
              description="most elusive pro skater to ever live",
              category=category3)

session.add(Item1)
session.commit()

Item2 = Items(user_id=1,
              item="bones bearings",
              description="the best bearings",
              category=category3)

session.add(Item2)
session.commit()

Item3 = Items(user_id=1,
              item="independent trucks",
              description="the best trucks",
              category=category3)

session.add(Item3)
session.commit()


print "added items!"
