# IAM-Bridge Integration

This document describes the steps to Install the `IAM-Bridge` Chart for the integration between IBM Cloud Pak® for Security and IBM Security Verify® instance.

# Summary

1. [Pre-Requisites](#pre-requisites)
1. [IAM-Bridge Chart Deployment](#iam-Bridge-chart-deployment)
1. [Verify and CP4S Integration](#verify-and-cp4s-integration)

## Pre-Requisites

1. Ensure you have [helm 3](https://www.ibm.com/docs/en/cloud-paks/cp-security/1.7.0?topic=tasks-installing-developer-tools#helm-v324) installed in your PATH.

2. Ensure you have [cloudctl](https://www.ibm.com/docs/en/cloud-paks/cp-security/1.7.0?topic=tasks-installing-developer-tools#cloudpak-cli) installed in your PATH.

3. Ensure you are authenticated with an administrator user in your Openshift 4.6+ cluster.

4. Ensure you have `python3` installed in your PATH along with Ansible, which can be installed with `pip3 install ansible`.

## IAM-Bridge Chart Deployment

To deploy the Chart:

1. Set the required Environment variables.

```
    VERIFY_CONNECTION_NAME="IAM-Bridge"
    VERIFY_URL=<YOUR_VERIFY_URL>    
    VERIFY_CLIENT_ID=<YOUR_CLIENT_ID>
    VERIFY_CLIENT_SECRET=<YOUR_CLIENT_SECRET>
    CP4S_NAMESPACE=<CP4S_NAMESPACE>
```

2. Clone the repository containing the IAM-Bridge Chart and change directory.

    ```
    git clone https://github.com/BRODERICKAL/ldap-bridge.git bridge

    cd bridge/
    ```

3.  Update the chart's values.yaml file.

    ```
    sed -i.bak -e "s#{{ VERIFY_URL }}#${VERIFY_URL}#; s#{{ VERIFY_CLIENT_ID }}#${VERIFY_CLIENT_ID}#; s#{{ VERIFY_CLIENT_SECRET }}#${VERIFY_CLIENT_SECRET}#" iam-bridge-chart/values.yaml
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

1. Change directory and update the playbook.yaml file

    ```
    cd iam-bridge-ansible/

    sed -i.bak -e "s#{{ VERIFY_URL }}#${VERIFY_URL}#; s#{{ VERIFY_CLIENT_ID }}#${VERIFY_CLIENT_ID}#; s#{{ VERIFY_CLIENT_SECRET }}#${VERIFY_CLIENT_SECRET}#; s#{{ CP4S_NAMESPACE }}#${CP4S_NAMESPACE}#; s#{{ VERIFY_CONNECTION_NAME }}#${VERIFY_CONNECTION_NAME}#" playbook.yaml
    ```

2. Run the ansible playbook

    ```
    python3 $(which ansible-playbook) -i hosts playbook.yaml
    ```