from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Categories, Items


engine = create_engine('sqlite:///project3rd.db')
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


#Category for Snowboarding
category1 = Categories(category = "Snowboarding", description = "extreme downhill sport on snow")

session.add(category1)
session.commit()


Item1 = Items(item = "Burton Custom", description = "all terrain freestyle board",  category = category1)

session.add(Item1)
session.commit()

Item2 = Items(item = "Burton Vapor", description = "The only board Erik Brown will ride",  category = category1)

session.add(Item2)
session.commit()

Item3 = Items(item = "Lobster snowboard", description = "Haldor jibs on this",  category = category1)

session.add(Item3)
session.commit()

#cateogory for surfing
category2 = Categories(category = "Surfing", description = "Riding ocean waves as they break on a board with fins")

session.add(category2)
session.commit()


Item1 = Items(item = "Al Merrick flyer", description = "good all around board",  category = category2)

session.add(Item1)
session.commit()

Item2 = Items(item = "Costco Wavestorm", description = "the best board out there. period.",  category = category2)

session.add(Item2)
session.commit()

Item3 = Items(item = "lost round nose fish", description = "everyone needs this in their quiver",  category = category2)

session.add(Item3)
session.commit()


#category for skateboarding
category3 = Categories(category = "Skateboarding", description = "surfing on concrete")

session.add(category3)
session.commit()


Item1 = Items(item = "Tom Penny board", description = "most elusive pro skater to ever live",  category = category3)

session.add(Item1)
session.commit()

Item2 = Items(item = "bones bearings", description = "the best bearings",  category = category3)

session.add(Item2)
session.commit()

Item3 = Items(item = "independent trucks", description = "the best trucks",  category = category3)

session.add(Item3)
session.commit()


print "added menu items!"
