Membership:
    slug
    price 
    type( free, pro, engerprise)
    stryp plac id

UserMembership:
    user                (foreignkey to default user)
    customer stripe id 
    membership type     (foreignkey to Membersip)

Subscription:
    user membership .
    stryp subscription id  (foreignkey to userMembersip)
    active 

Course:
    slug
    title
    description
    allowed membersip

Lesson
    title 
    slug
    course              (foreignkey to Corse)
    thumbnail
    