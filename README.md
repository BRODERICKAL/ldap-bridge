# IAM-Bridge Integration

This document describes the steps to Install the `IAM-Bridge` Chart for the integration between IBM Cloud Pak® for Security and IBM Security Verify® instance.

# Summary

1. [Pre-Requisites](#pre-requisites)
1. [IAM-Bridge Chart Deployment](#iam-Bridge-chart-deployment)
1. [Verify and CP4S Integration](#verify-and-cp4s-integration)

## Pre-Requisites

1. Ensure you have [helm 3](https://www.ibm.com/docs/en/cloud-paks/cp-security/1.7.0?topic=tasks-installing-developer-tools#helm-v324) installed in your PATH.

2. Ensure you are authenticated with an administrator user in your Openshift 4.6+ cluster.

## IAM-Bridge Chart Deployment

To deploy the Chart:

1. Set the required Environment variables.

```
    VERIFY_URL=<YOUR_VERIFY_URL>
    VERIFY_CLIENT_ID=<YOUR_CLIENT_ID>
    VERIFY_CLIENT_SECRET=<YOUR_CLIENT_SECRET>
    CP4S_NAMESPACE=<CP4S_NAMESPACE>
```

2. Clone the repository containing the IAM-Bridge Chart.

    ```
    git clone https://github.com/BRODERICKAL/ldap-bridge.git bridge
    ```

3.  Update the chart's values.yaml file.

    ```
    sed -i '' "s#{{ VERIFY_URL }}#${VERIFY_URL}#; s#{{ VERIFY_CLIENT_ID }}#${VERIFY_CLIENT_ID}#; s#{{ VERIFY_CLIENT_SECRET }}#${VERIFY_CLIENT_SECRET}#" iam-bridge-chart/values.yaml
    ```

4. Install the Chart.

    ```
    helm upgrade --install cp4s-saas-iam-bridge-chart --namespace=${CP4S_NAMESPACE} ./iam-bridge-chart --reset-values --debug
    ```

5. Confirm the `iam-bridge` pods are running.

    ```
    oc get pod -n ${CP4S_NAMESPACE} -lapp=iam-bridge

    NAME                          READY   STATUS    RESTARTS   AGE
    iam-bridge-5d6b987ccf-9bzw6   1/1     Running   0          3h29m    
    ```

## IBM Cloud Pak for Security and IBM Security Verify Integration

Once the IAM-Bridge Chart is deployed, the integration between IBM Security Verify and the Cloud Pak for Security instance must be setup.

1. Update the playbook.yaml file

    ```
    sed -i '' "s#{{ VERIFY_URL }}#${VERIFY_URL}#; s#{{ VERIFY_CLIENT_ID }}#${VERIFY_CLIENT_ID}#; s#{{ VERIFY_CLIENT_SECRET }}#${VERIFY_CLIENT_SECRET}#; s#{{ CP4S_NAMESPACE }}#${CP4S_NAMESPACE}#" playbook.yaml
    ```

2. Run the ansible playbook

    ```
    ansible-playbook -i hosts playbook.yaml
    ```