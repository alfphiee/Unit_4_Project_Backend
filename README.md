# breakDOWN - Project Four (GA)

This project was completed at the end of Unit 4 of the Software Engineering Immersive Course. The current focus was Django and the goal of the project was to produce a Frontend & Backend for a site that would allow for CRUD Operations. In this project I created a tool that could be used for planning out future projects - allowing for the creation and tracking of tasks.

## Deployment

This project was deployed using Netlify and is available [here](https://breakdown-alfie.netlify.app/)

## Getting Started

This project is separated into two repositories

- [Frontend](https://github.com/alfphiee/Unit_4_Project_Frontend)
- Backend (this repo)

To run the backend:

1.  Clone this repository
2.  In CLI run `pip install requirements.txt` on the root folder to install the required dependencies
3.  Next in the CLI run `python3 manage.py runserver` to run the backend in your local environment

## Timeframe & Working Team

We had a week to complete this project, working solo.

## Technologies Used

- Node.js
- PostgreSQL
- React.js
- DaisyUI
- Tailwind CSS
- react-router-dom
- react-beautiful-dnd
- jwt
- Git

## Brief

- Be a full-stack **Django/React** application.
- Connect to and perform data operations on a **PostgreSQL** database (the default SQLLite3 database is not acceptable).
- If consuming an API (OPTIONAL), have at least **one data entity** (Model) in addition to the built-in User model. The related entity can be either a **one-to-many (1:M) or a many-to-many (M:M)** relationship.
- If not consuming an API, have at least **two data entities** (Models) in addition to the built-in User model. It is preferable to have at least **one one-to-many (1:M) and one many-to-many (M:M)** relationship between entities/models.
- Have **full-CRUD data operations** across any combination of the app's models (excluding the User model). For example, creating/reading/updating posts and creating/deleting comments qualifies as full-CRUD data operations.
- **Authenticate users using Django's built-in authentication**.
- **Implement authorization by restricting access to the Creation, Updating & Deletion of data resources** using the `login_required` decorator in the case of view functions; or, in the case of class-based views, inheriting from the `LoginRequiredMixin` class.
- Be **deployed online** Presentations must use the deployed application.

## Planning

Started by creating an ERD using Lucidchart

![ERD-Diagram](https://i.imgur.com/P3bioxB.png)

I then created a basic wireframe diagram to get an idea of the flow & layout of the site:

![Wireframe](https://i.imgur.com/Zu2ZUkN.png)

I then created some basic User Stories which I track on a Trello board to keep up to date with the current status:

![Trello-board](https://imgur.com/ckJYtg8.png)

## Build/Code Process

I started off by implementing the basic endpoints that would be 100% necessary

```python
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user.id
        return Project.objects.filter(Q(owner=user) | Q(collaborators=user)).distinct()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_context(self):
        return {'project_id': self.kwargs['project_pk']}

class UserTasksViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        user = self.request.user.id
        return Task.objects.filter(assignee=user)
```

Using Django-rest-framework I set up views for my main models. For projects I filtered the data to only bring back projects that the user was the owner or a collaborator on.

I created two versions of the Task View Set - this is due to the fact I wanted to have two ways for a user to view tasks:
View all Tasks (including other collaborators) on a specific project
View all of their own Tasks across multiple projects

TaskViewSet is used to pull all tasks for a project - this is what a user will see when they go in to view details on a specific project

UserTasksViewSet pulls the tasks just for that user - this will populate the table the user will see when they click ‘My Tasks’

```python
class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators_emails = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    collaborators = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'github_url', 'created_at', 'updated_at', 'owner', 'collaborators', 'collaborators_emails']

    def create(self, validated_data):
        collaborators_emails = validated_data.pop('collaborators_emails', [])
        user = self.context['request'].user
        project = Project.objects.create(**validated_data, owner=user)
        self._update_collaborators(project, collaborators_emails)
        return project

    def update(self, instance, validated_data):
        collaborators_emails = validated_data.pop('collaborators_emails', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._update_collaborators(instance, collaborators_emails)
        return instance

    def _update_collaborators(self, project, emails):
        if emails:
            collaborators = []
            for email in emails:
                try:
                    user = User.objects.get(email=email)
                    collaborators.append(user)
                except User.DoesNotExist:
                    pass
            project.collaborators.set(collaborators)
```

I had to manually create a few methods specifically for the Serializers. I created a specific function which would handle the addition of collaborators - I wanted to allow the user to enter emails of collaborators on both creation and updating. I allow users to enter a comma separated list of collaborators which I then loop through to search for the matching Users in the DB before adding these users as collaborators to the project.

## Challenges

- An initial challenge I ran into was a difficulty in understanding how to change the basic functionality of django-rest-framework - I found it very easy to set up for basic GET, PUT, CREATE, DELETE requests but when I wanted to personalise these a little more to fit my project I had to really take my time to read through the documentation - this was good as it made me a lot more comfortable reading through documentation.
- Another challenge I faced was I was initially a bit too ambitious with the functionality I wanted to add - following working in a group project I thought I would be able to complete a lot more in the timeframe - this meant I had to trim back a few features - luckily I had already a good idea of what features were ‘Must Have’ for my application to be in a state I was happy with.

## Wins

One major Win I had was adding the ability to drag & drop tasks between swimlanes to update the status:

![drag-and-drop](https://imgur.com/Io0VqpG.png)

Using react-beautiful-dnd I managed to make it so the task cards were drag and droppable:

```jsx
<DragDropContext onDragEnd={onDragEnd}>
  <div className="flex h-full justify-around align-center items-start">
    {["TD", "IP", "CO"].map((status, index) => (
      <Droppable key={status} droppableId={status}>
        {(provided) => (
          <div
            className="w-full mx-2 h-full flex flex-col items-center"
            ref={provided.innerRef}
            {...provided.droppableProps}
          >
            {tasksByStatus(status).map((task, index) => (
              <Draggable
                className="w-full"
                key={task.id.toString()}
                draggableId={task.id.toString()}
                index={index}
              >
                {(provided) => (
                  <div
                    className="w-full"
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                  >
                    <TaskView
                      assignees={assignees}
                      editTaskList={editTaskList}
                      task={task}
                    />
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    ))}
  </div>
</DragDropContext>
```

## Key Learnings

- This project taught me the importance of prioritisation - it’s not necessarily a bad thing planning too much functionality as long as you have a good understanding of what the key features are and ensure they are achievable in the timeframe
- I also learnt the importance of reading documentation and also how useful well written documentation is. Although in the past I had read documentation - it was mainly just to pull in a single function at a time etc. for this project I had to have a much more thorough understanding of django-rest-framework

## Future Improvements

- I would like to add the additional models listed in my ERD - such as adding the ability to add comments to tasks, to allow users to hand tasks between each other and add notes regarding their current progress / findings
- I’d also like to add the ability to add tags to tasks - to allow for filtering of tasks. In a bigger project their might be certain tasks that a person has no interest in as they aren’t part of their domain - having tags would allow for ease of filtering
