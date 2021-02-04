#  -*- coding: iso-8859-1 -*-
# Copyright (C) 2021  CEA/DEN, EDF R&D, OPEN CASCADE
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.salome-platform.org/ or email : webmaster.salome@opencascade.com
#

def buildInstance(orb):
    from SHAPERSTUDY import SHAPERSTUDY_No_Session
    from SALOME_ContainerPy import SALOME_ContainerPy_Gen_i
    import PortableServer
    import KernelServices
    obj = orb.resolve_initial_references("RootPOA")
    poa = obj._narrow(PortableServer.POA)
    pman = poa._get_the_POAManager()
    #
    cont = SALOME_ContainerPy_Gen_i(orb,poa,"FactoryServer")
    conId = poa.activate_object(cont)
    conObj = poa.id_to_reference(conId)
    #
    pman.activate()
    #
    compoName = "SHAPERSTUDY"
    servant = SHAPERSTUDY_No_Session(orb,poa,conObj,"FactoryServer","SHAPERSTUDY_inst_1",compoName)
    ret = servant.getCorbaRef()
    KernelServices.RegisterCompo(compoName,ret)
    return ret, orb
