#!/usr/bin/env python
#
# Copyright 2014 tigmi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kubernetes import simplejson
import re

class RestartPolicyAlways(object):
    """A Class representing the RestartPolicyAlways structure used by the kubernetes API

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete RestartPolicyAlways.
        '''

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return True

    def __str__(self):
        '''A string representation of this Kubernetes.RestartPolicyAlways instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.RestartPolicyAlways instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.RestartPolicyAlways instance.

        Returns:
          A JSON string representation of this kubernetes.RestartPolicyAlways instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.RestartPolicyAlways instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.RestartPolicyAlways instance
        '''
        data = {}
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.RestartPolicyAlways instance
        '''
        return RestartPolicyAlways()

class RestartPolicyOnFailure(object):
    """A Class representing the RestartPolicyOnFailure structure used by the kubernetes API

        TODO(dchen1107): Define what kinds of failures should restart.
        TODO(dchen1107): Decide whether to support policy knobs, and, if so, which ones.
    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete RestartPolicyOnFailure.
        '''

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return True

    def __str__(self):
        '''A string representation of this Kubernetes.RestartPolicyOnFailure instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.RestartPolicyOnFailure instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.RestartPolicyOnFailure instance.

        Returns:
          A JSON string representation of this kubernetes.RestartPolicyOnFailure instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.RestartPolicyOnFailure instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.RestartPolicyOnFailure instance
        '''
        data = {}
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.RestartPolicyOnFailure instance
        '''
        return RestartPolicyOnFailure()


class RestartPolicyNever(object):
    """A Class representing the RestartPolicyNever structure used by the kubernetes API

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete RestartPolicyNever.
        '''

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return True

    def __str__(self):
        '''A string representation of this Kubernetes.RestartPolicyNever instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.RestartPolicyNever instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.RestartPolicyNever instance.

        Returns:
          A JSON string representation of this kubernetes.RestartPolicyNever instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.RestartPolicyNever instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.RestartPolicyNever instance
        '''
        data = {}
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.RestartPolicyNever instance
        '''
        return RestartPolicyNever()


class RestartPolicy(object):
    """A Class representing the RestartPolicy structure used by the kubernetes API

    The RestartPolicy structure exposes the following properties:

    RestartPolicy.Always
    RestartPolicy.OnFailure
    RestartPolicy.Never

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete RestartPolicy.

        Arg:

         Always:
         OnFailure:
         Never:
             Only one of the following restart policies may be specified.
            If none of the following policies is specified, the default one
            is RestartPolicyAlways.

        '''

        param_defaults = {
            'Always':                         None,
            'OnFailure':                     None,
            'Never':                         None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Always == other.Always and \
            self.OnFailure == other.OnFailure and \
            self.Never == other.Never
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.RestartPolicy instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.RestartPolicy instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.RestartPolicy instance.

        Returns:
          A JSON string representation of this kubernetes.RestartPolicy instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.RestartPolicy instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.RestartPolicy instance
        '''
        data = {}
        if self.Always:
            data['always'] = self.Always.AsDict()
        if self.OnFailure:
            data['onFailure'] = self.OnFailure.AsDict()
        if self.Never:
            data['never'] = self.Never.AsDict()
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.RestartPolicy instance
        '''

        always = None
        onFailure = None
        never = None

        if 'always' in data:
            from kubernetes import RestartPolicyAlways
            always = RestartPolicyAlways.NewFromJsonDict(data['always'])

        if 'onFailure' in data:
            from kubernetes import RestartPolicyOnFailure
            onFailure = RestartPolicyOnFailure.NewFromJsonDict(data['onFailure'])

        if 'never' in data:
            from kubernetes import RestartPolicyNever
            never = RestartPolicyNever.NewFromJsonDict(data['never'])

        return RestartPolicy(
                    Always=always,
                    OnFailure=onFailure,
                    Never=never)

class PodState(object):
    """A Class representing the PodState structure used by the kubernetes API

    PodState is the state of a pod, used as either input (desired state) or output (current state).

    The PodState structure exposes the following properties:

    PodState.Phase
    PodState.Conditions
    PodState.HostIP
    PodState.PodIP
    PodState.StartTime
    PodState.ContainerStatuses

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete PodState.

        Arg:

         HostIP:
         Conditions:
         PodIP:

        '''

        param_defaults = {
            'Phase':            None,
            'Conditions':       None,
            'HostIP':           None,
            'PodIP':            None,
            'StartTime':        None,
            'ContainerStatuses': None,
        }

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Phase == other.Phase and \
            self.Conditions == other.Conditions and \
            self.HostIP == other.HostIP and \
            self.PodIP == other.PodIP and \
            self.StartTime == other.StartTime and \
            self.ContainerStatuses == other.ContainerStatuses
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.PodState instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.PodState instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.PodState instance.

        Returns:
          A JSON string representation of this kubernetes.PodState instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.PodState instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.PodState instance
        '''

        data = {}
        if self.Phase:
            data['phase'] = self.Phase
        if self.HostIP:
            data['hostIP'] = self.HostIP
        if self.PodIP:
            data['podIP'] = self.PodIP
        if self.Conditions:
            data['conditions'] = self.Conditions
        if self.ContainerStatuses:
            data['ContainerStatuses'] = self.ContainerStatuses

        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.PodState instance
        '''
        return PodState(Phase=data.get('phase', None),
                        Conditions=data.get('conditions', None),
                        HostIP=data.get('hostIP', None),
                        PodIP=data.get('podIP', None),
                        ContainerStatuses=data.get('containerStatuses', None),
                        StartTime=data.get('startTime', None))

from kubernetes import TypeMeta
class PodList(TypeMeta):
    """A Class representing the PodList structure used by the kubernetes API

    PodList is a list of Pods.

    The PodList structure exposes the following properties:

    PodList.Items

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete PodList.

        Arg:

         Items:

        '''

        param_defaults = {
            'Items':                     None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

        super(PodList, self).__init__(**kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Items == other.Items and \
            super(PodList, self).__eq__(other)
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.PodList instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.PodList instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.PodList instance.

        Returns:
          A JSON string representation of this kubernetes.PodList instance.
        '''
        return simplejson.dumps(dict(self.AsDict().items()+super(PodList, self).AsDict().items()), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.PodList instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.PodList instance
        '''
        data = {}
        if self.Items:
            data['items'] = [pod.AsDict() for pod in self.Items]
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.PodList instance
        '''

        items = []
        metadata = data.get('metadata')

        if 'items' in data and data['items']:
            from kubernetes import Pod
            items = [Pod.NewFromJsonDict(pod) for pod in data['items']]

        return PodList(
                    Kind=data.get('kind', None),
                    APIVersion=data.get('apiVersion', None),
                    CreationTimestamp=metadata.get('creationTimestamp', None),
                    SelfLink=metadata.get('selfLink', None),
                    ResourceVersion=metadata.get('resourceVersion', None),
                    Name=metadata.get('name', None),
                    UID=metadata.get('uid', None),
                    Namespace=metadata.get('namespace', None),
                    Annotations=metadata.get('annotations', None),

                    Items=items)

class ContainerSpec:
    def __init__(self, json):
        self.Name = json['name']
        self.Image = json['image']
        self.MemLimit = 0.0
        try:
            self.MemLimit = self.__convert_mem_str_to_int__(json['resources']['limits']['memory'])
        except Exception, e:
            pass

    def __convert_mem_str_to_int__(self, mem_str):
        match = re.match('^[0-9]*', mem_str)
        if match is None:
            return 0.0
        value = float(mem_str[match.start():match.end()])
        unit = mem_str[match.end():]
        if unit == 'Gi':
            value = value * 1024.0
        if unit == 'G':
            value = value * pow(10,9) / 1024 / 1024
        if unit == 'M':
            value = value * pow(10,6) / 1024 / 1024
        if unit == 'Mi':
            pass
        if unit == 'K':
            value = value * pow(10,3) / 1024 / 1024
        if unit == 'Ki':
            value = value / 1024

        return round(value, 2)

class Pod(TypeMeta):
    """A Class representing the Pod structure used by the kubernetes API

    Pod is a collection of containers, used as either input (create, update) or as output (list, get).

    The Pod structure exposes the following properties:

    Pod.Labels
    Pod.DesiredState
    Pod.CurrentState

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete Pod.

        Arg:

         Labels:
         DesiredState:
         CurrentState:

        '''

        param_defaults = {
            'Labels':                             None,
            'DesiredState':                     None,
            'CurrentState':                     None,
            'Status':                     None,
            'NodeName':     None,
            'ContainerSpecs': None,
            '': None,}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

        super(Pod, self).__init__(**kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Labels == other.Labels and \
            self.DesiredState == other.DesiredState and \
            self.CurrentState == other.CurrentState and \
            self.Status == other.Status and \
            super(Pod, self).__eq__(other)
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.Pod instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.Pod instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.Pod instance.

        Returns:
          A JSON string representation of this kubernetes.Pod instance.
        '''
        return simplejson.dumps(dict(self.AsDict().items()+super(Pod, self).AsDict().items()), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.Pod instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.Pod instance
        '''
        data = super(Pod, self).AsDict()
        if self.Labels:
            data['labels'] = self.Labels
        if self.DesiredState:
            data['desiredState'] = self.DesiredState.AsDict()
        if self.CurrentState:
            data['currentState'] = self.CurrentState.AsDict()
        if self.Status:
            data['status'] = self.Status.AsDict()
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.Pod instance
        '''

        desiredState = None
        currentState = None
        state = None
        condition = None
        nodeName = None
        containerSpecs = None

        metadata = data.get('metadata', None)
        status = data.get('status', None)

        if 'desiredState' in data:
            from kubernetes import PodState
            desiredState = PodState.NewFromJsonDict(data['desiredState'])

        if 'currentState' in data:
            from kubernetes import PodState
            currentState = PodState.NewFromJsonDict(data['currentState'])

        if 'status' in data:
            from kubernetes import PodState
            state = PodState.NewFromJsonDict(data['status'])
            nodeName = state.HostIP

        if nodeName is None and 'spec' in data:
            nodeName = data['spec'].get('nodeName', None)

        try:
            if len(data['spec']['containers']) > 0:
                containerSpecs = []
                for container in data['spec']['containers']:
                    containerSpec = ContainerSpec(container)
                    containerSpecs.append(containerSpec)
        except:
            containerSpecs = None

        return Pod(
                    Kind=data.get('kind', None),
                    APIVersion=data.get('apiVersion', None),
                    Name=metadata.get('name', None),
                    UID=metadata.get('uid', None),
                    CreationTimestamp=metadata.get('creationTimestamp', None),
                    SelfLink=metadata.get('selfLink', None),
                    ResourceVersion=metadata.get('resourceVersion', None),
                    Namespace=metadata.get('namespace', None),
                    Annotations=metadata.get('annotations', None),
                    Labels=metadata.get('labels', None),
                    Status=state,
                    DesiredState=desiredState,
                    CurrentState=currentState,
                    NodeName=nodeName,
                    ContainerSpecs = containerSpecs)

    @property
    def MemLimit(self):
        if self.ContainerSpecs is None:
            return 0.0
        
        memLimit = 0.0
        for containerSpec in self.ContainerSpecs:
            memLimit = memLimit + containerSpec.MemLimit

        return memLimit

class ReplicationControllerSpec(object):
    """A Class representing the ReplicationControllerSpec structure used by the kubernetes API

    ReplicationControllerSpec is the state of a pod, used as either input (desired state) or output (current state).

    The ReplicationControllerSpec structure exposes the following properties:

    ReplicationControllerSpec.Replicas
    ReplicationControllerSpec.ReplicaSelector
    ReplicationControllerSpec.PodTemplate

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete ReplicationControllerSpec.

        Arg:
         Replicas:
         ReplicaSelector
         PodTemplate:


        '''

        param_defaults = {
            'Replicas':                         None,
            'ReplicaSelector':                     None,
            'PodTemplate':                         None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Replicas == other.Replicas and \
            self.ReplicaSelector == other.ReplicaSelector and \
            self.PodTemplate == other.PodTemplate
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.ReplicationControllerSpec instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.ReplicationControllerSpec instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.ReplicationControllerSpec instance.

        Returns:
          A JSON string representation of this kubernetes.ReplicationControllerSpec instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.ReplicationControllerSpec instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.ReplicationControllerSpec instance
        '''
        data = {}
        if self.Replicas:
            data['replicas'] = self.Replicas
        if self.ReplicaSelector:
            data['selector'] = self.ReplicaSelector
        if self.PodTemplate:
            data['template'] = self.PodTemplate.AsDict()
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.ReplicationControllerSpec instance
        '''

        podTemplate = None
        selector = data.get('selector')

        # TODO: 'podTemplate' should be replaced by 'template'
        if 'podTemplate' in data:
            from kubernetes import PodTemplate
            podTemplate = PodTemplate.NewFromJsonDict(data['podTemplate'])

        return ReplicationControllerSpec(
                    Replicas=data.get('replicas', None),
                    ReplicaSelector=selector,
                    PodTemplate=podTemplate)


class ReplicationControllerList(TypeMeta):
    """A Class representing the ReplicationControllerList structure used by the kubernetes API

    ReplicationControllerList is a collection of replication controllers.

    The ReplicationControllerList structure exposes the following properties:

    ReplicationControllerList.Items

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete ReplicationControllerList.

        Arg:

         Items:

        '''

        param_defaults = {
            'Items':                             None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

        super(ReplicationControllerList, self).__init__(**kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.Items == other.Items and \
            super(ReplicationControllerList, self).__eq__(other)
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.ReplicationControllerList instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.ReplicationControllerList instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.ReplicationControllerList instance.

        Returns:
          A JSON string representation of this kubernetes.ReplicationControllerList instance.
        '''
        return simplejson.dumps(dict(self.AsDict().items()+super(ReplicationControllerList, self).AsDict().items()), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.ReplicationControllerList instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.ReplicationControllerList instance
        '''
        data = {}
        if self.Items:
            data['items'] = [replicationController.AsDict() for replicationController in self.Items]
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.ReplicationControllerList instance
        '''

        items = []
        metadata = data.get('metadata')

        if 'items' in data:
            from kubernetes import ReplicationController
            items = [ReplicationController.NewFromJsonDict(r) for r in data['items']]

        return ReplicationControllerList(
                    Kind=data.get('kind', None),
                    APIVersion=data.get('apiVersion', None),
                    Name=metadata.get('name', None),
                    UID=metadata.get('uid', None),
                    CreationTimestamp=metadata.get('creationTimestamp', None),
                    SelfLink=metadata.get('selfLink', None),
                    ResourceVersion=metadata.get('resourceVersion', None),
                    Namespace=metadata.get('namespace', None),
                    Annotations=metadata.get('annotations', None),

                    Items=items)


class ReplicationController(TypeMeta):
    """A Class representing the ReplicationController structure used by the kubernetes API

    ReplicationController represents the configuration of a replication controller.

    The ReplicationController structure exposes the following properties:

    ReplicationController.DesiredState
    ReplicationController.CurrentState
    ReplicationController.Labels

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete ReplicationController.

        Arg:

         DesiredState:
         CurrentState:
         Labels:

        '''

        param_defaults = {
            'DesiredState':                             None,
            'CurrentState':                             None,
            'Spec':                             None,
            'Labels':                                     None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

        super(ReplicationController, self).__init__(**kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.DesiredState == other.DesiredState and \
            self.CurrentState == other.CurrentState and \
            self.Labels == other.Labels and \
            self.Spec == other.Spec and \
            super(ReplicationController, self).__eq__(other)
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.ReplicationController instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.ReplicationController instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.ReplicationController instance.

        Returns:
          A JSON string representation of this kubernetes.ReplicationController instance.
        '''
        return simplejson.dumps(dict(self.AsDict().items()+super(ReplicationController, self).AsDict().items()), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.ReplicationController instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.ReplicationController instance
        '''
        data = super(ReplicationController, self).AsDict()
        if self.DesiredState:
            data['desiredState'] = self.DesiredState
        if self.CurrentState:
            data['currentState'] = self.CurrentState
        if self.Labels:
            data['labels'] = self.Labels
        if self.Spec:
            data['spec'] = self.Spec.AsDict()
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.ReplicationController instance
        '''

        desiredState = None
        currentState = None
        metadata = data.get('metadata')

        if 'desiredState' in data:
            from kubernetes import ReplicationControllerSpec
            desiredState = ReplicationControllerSpec.NewFromJsonDict(data['desiredState'])

        if 'currentState' in data:
            from kubernetes import ReplicationControllerSpec
            currentState = ReplicationControllerSpec.NewFromJsonDict(data['currentState'])

        if 'spec' in data:
            from kubernetes import ReplicationControllerSpec
            spec = ReplicationControllerSpec.NewFromJsonDict(data['spec'])
            if spec.Replicas:
                desiredState = spec.Replicas

        if 'status' in data and 'replicas' in data['status']:
            currentState = data['status'].get('replicas')
        return ReplicationController(
                    Spec=spec,
                    Kind=data.get('kind', None),
                    APIVersion=data.get('apiVersion', None),
                    Name=metadata.get('name', None),
                    UID=metadata.get('uid', None),
                    CreationTimestamp=metadata.get('creationTimestamp', None),
                    SelfLink=metadata.get('selfLink', None),
                    ResourceVersion=metadata.get('resourceVersion', None),
                    Namespace=metadata.get('namespace', None),
                    Annotations=metadata.get('annotations', None),
                    Labels=metadata.get('labels', None),
                    DesiredState=desiredState,
                    CurrentState=currentState)

class PodTemplate(object):
    """A Class representing the PodTemplate structure used by the kubernetes API

    PodTemplate holds the information used for creating pods.

    The PodTemplate structure exposes the following properties:

    PodTemplate.DesiredState
    PodTemplate.Labels

    """
    def __init__(self, **kwargs):
        '''An object to hold a Kubernete PodTemplate.

        Arg:
         DesiredState:
         Labels


        '''

        param_defaults = {
            'DesiredState':                         None,
            'Labels':                                 None}

        for (param, default) in param_defaults.iteritems():
            setattr(self, param, kwargs.get(param, default))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            return other and \
            self.DesiredState == other.DesiredState and \
            self.Labels == other.Labels
        except AttributeError:
            return False

    def __str__(self):
        '''A string representation of this Kubernetes.PodTemplate instance.

        The return value is the same as the JSON string representation.

        Returns:
         A string representation of this kubernetes.PodTemplate instance.
        '''
        return self.AsJsonString()

    def AsJsonString(self):
        '''A JSON string representation of this kubernetes.PodTemplate instance.

        Returns:
          A JSON string representation of this kubernetes.PodTemplate instance.
        '''
        return simplejson.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        ''' A dic representation of this kubernetes.PodTemplate instance.

        The return values uses the same key names as the JSON representation.

        Returns:
          A dict representing this kubernetes.PodTemplate instance
        '''
        data = {}
        if self.DesiredState:
            data['desiredState'] = self.DesiredState.AsDict()
        if self.Labels:
            data['labels'] = self.Labels
        return data

    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance base on a JSON dict
        Args:
          data: A JSON dict, as converted from the JSON in the kubernetes API
        Returns:
          A kubernetes.PodTemplate instance
        '''

        desiredState = None
        if 'desiredState' in data:
            from kubernetes import PodState
            desiredState = PodState.NewFromJsonDict(data['desiredState'])

        return PodTemplate(
                    DesiredState=desiredState,
                    Labels=data.get('labels', None))
